import sys
import os
import re

# The Simple Programming Language

file_source = sys.argv[1]

loopmod = False

if len(sys.argv) >= 3:
    if sys.argv[2] == "-loopmod":
        loopmod = True

variables = {}
importfile = []
functions = {
    '__init__': ['print("program init")'],
}

def isVariableInList(var_name):
    return var_name in variables

def getValueByKey(var_name):
    if var_name in variables:
        return variables[var_name]
    else:
        return None # This line should never be executed

a = open(file_source, "r")

ab = a.readlines()
for line in ab:
    if line.startswith("import"):
        pattern = r'(\w+|\(|\)|".*?")'
        tokens = re.findall(pattern, line)
        tokens[1] = tokens[1].replace('"', '')
        importfile.append(tokens[1])
    else:
        pass

a.close()

i = open(file_source, "r")
u = i.read()
i.close()

allcode = "# Generated File from SPL\n"
for code in importfile:
    with open(code, "r+") as f:
        af = f.read()
        allcode += af + "\n"

allcode += u

b = open(file_source + ".gen", "w")
b.write(allcode)
b.close()

def executeCode(file_source):
    in_function = False
    in_if = False
    is_if_valid = None
    wcondition = False
    file = open(file_source, "r+")
    files = file.readlines()
    for line in files:
        if line.startswith("#"):
            pass
        elif line.startswith("\n"):
            pass
        elif line.startswith("var"):
            splitline = line.split()
            if splitline[2] != "=":
                print(f"Incorrect variable declaration here : '{line}'")
                exit(1)
            # Determinate if the variable content is a STRING or INTEGER or a VARIABLE VALUE.
            if splitline[3].startswith('"'):
                stringQuote = '"'
                if stringQuote in splitline[3]:
                    splitline[3] = splitline[3].replace('"', '')
                    variables[splitline[1]] = splitline[3]
            elif splitline[3].isdigit():
                variables[splitline[1]] = splitline[3]
                pass
            elif splitline[3] == splitline[1]:
                print(f"Variable name and variable value are the same here : '{line}'")
                exit(1)
            elif isVariableInList(splitline[3]):
                variables[splitline[1]] = getValueByKey(splitline[3])
            elif splitline[3].startswith("input"):
                index = 8
                pattern = r'\b\w+\b|\S|\s'
                tokens = re.findall(pattern, line)
                stringList = ""
                while index < len(tokens) and tokens[index] != ')':
                    stringList += tokens[index]
                    index = index + 1
                stringQuote = '"'
                if stringQuote in stringList:
                    stringList = stringList.replace('"', '')
                a = input(stringList)
                variables[splitline[1]] = a
            else:
                print(f"Undefined variable value here : '{line}'")
                exit(1)
        elif line.startswith("print"):
            pattern = r'(\w+|\(|\)|".*?")'
            tokens = re.findall(pattern, line)
            index = 2
            stringList = ""
            while index < len(tokens) and tokens[index] != ')':
                if '"' in tokens[index]:
                    a = tokens[index].replace('"', '')
                    stringList += a
                elif tokens[index].isdigit():
                    stringList += tokens[index]
                elif isVariableInList(tokens[index]):
                    stringList += getValueByKey(tokens[index])
                else:
                    print(f"Undefined content in print here : '{line}'")
                    exit(1)
                index = index + 1
            print(stringList)   
        elif line.startswith("function"):
            pattern = r'(\w+|\(|\)|".*?")'
            tokens = re.findall(pattern, line)
            in_function = True
            functions[tokens[1]] = None
        elif line.startswith("import"):
            pass
        elif line.startswith("exit"):
            pattern = r'(\w+|\(|\)|".*?")'
            tokens = re.findall(pattern, line)
            if tokens[2].isdigit():
                file.close()
                break
            else:
                print(f"Invalid value in exit here : '{line}'")
                exit(1)
        elif line.startswith(' '):
            if in_function:
                #print("ii")
                #print("last function declare : " + list(functions.keys())[-1])
                a = line.replace('    ', '', 1)
                key = list(functions.keys())[-1]
                if functions.get(key) is None:
                    functions[key] = [a]
                else:
                    functions[key] = [functions[key], a]
            elif in_if:
                ap = []
                a = line.replace('    ', '', 1)
                ap.append(a)
                executeFunctionCode(ap)
            else:
                pass
        elif line.startswith("end"):
            in_function = False
        elif line.startswith("fi"):
            in_if = False
        elif line.startswith("if"):
            result = re.findall(r'"\w+"|\w+|!=|==|<|>|\S', line)
            if (customif(result[2], result[3], result[4])):
                in_if = True
            else:
                in_if = False
        for key in functions:
            if line.startswith(key + "()"):
                a = functions.get(key)
                executeFunctionCode(a)
            elif line.startswith(key):
                print(f"<function: {key} defined in {functions}>")

def customif(elementToCompare, signToCompare, otherToCompare):
                acompare = ""
                if elementToCompare.startswith('"'):
                    stringQuote = '"'
                    elementToCompare = elementToCompare.replace('"', '')
                    acompare += elementToCompare
                elif elementToCompare.isdigit():
                    acompare += elementToCompare
                elif isVariableInList(elementToCompare):
                    acompare += getValueByKey(elementToCompare)

                bcompare = ""
                if otherToCompare.startswith('"'):
                    stringQuote = '"'
                    otherToCompare = otherToCompare.replace('"', '')
                    bcompare += otherToCompare
                elif otherToCompare.isdigit():
                    bcompare += otherToCompare
                elif isVariableInList(otherToCompare):
                    bcompare += getValueByKey(otherToCompare)

                if signToCompare == "==":
                    if acompare == bcompare:
                        return True
                    else:
                        return False
                
                if signToCompare == "!=":
                    if acompare != bcompare:
                        return True
                    else:
                        return False

                if signToCompare == "<":
                    if acompare < bcompare:
                        return True
                    else:
                        return False

                if signToCompare == ">":
                    if acompare > bcompare:
                        return True
                    else:
                        return False

def executeFunctionCode(a):
    for i in a:
        if i.startswith("#"):
            pass
        elif i.startswith("\n"):
            pass
        elif i.startswith("var"):
            splitline = i.split()
            if splitline[2] != "=":
                print(f"Incorrect variable declaration here : '{i}'")
                exit(1)
            # Determinate if the variable content is a STRING or INTEGER or a VARIABLE VALUE.
            if splitline[3].startswith('"'):
                stringQuote = '"'
                if stringQuote in splitline[3]:
                    splitline[3] = splitline[3].replace('"', '')
                    variables[splitline[1]] = splitline[3]
            elif splitline[3].isdigit():
                variables[splitline[1]] = splitline[3]
                pass
            elif splitline[3] == splitline[1]:
                print(f"Variable name and variable value are the same here : '{i}'")
                exit(1)
            elif isVariableInList(splitline[3]):
                variables[splitline[1]] = getValueByKey(splitline[3])
            elif splitline[3].startswith("input"):
                index = 8
                pattern = r'\b\w+\b|\S|\s'
                tokens = re.findall(pattern, i)
                stringList = ""
                while index < len(tokens) and tokens[index] != ')':
                    stringList += tokens[index]
                    index = index + 1
                stringQuote = '"'
                if stringQuote in stringList:
                    stringList = stringList.replace('"', '')
                a = input(stringList)
                variables[splitline[1]] = a
            else:
                print(f"Undefined variable value here : '{i}'")
                exit(1)
        elif i.startswith("print"):
            pattern = r'(\w+|\(|\)|".*?")'
            tokens = re.findall(pattern, i)
            index = 2
            stringList = ""
            while index < len(tokens) and tokens[index] != ')':
                if '"' in tokens[index]:
                    a = tokens[index].replace('"', '')
                    stringList += a
                elif tokens[index].isdigit():
                    stringList += tokens[index]
                elif isVariableInList(tokens[index]):
                    stringList += getValueByKey(tokens[index])
                else:
                    print(f"Undefined content in print here : '{i}'")
                    exit(1)
                index = index + 1
            print(stringList)
        for key in functions:
            if line.startswith(key + "()"):
                a = functions.get(key)
                executeFunctionCode(a)
            elif line.startswith(key):
                print(f"<function: {key} defined in {functions}>")

variables.clear()
if loopmod:
    while 1:
        executeCode(file_source + ".gen")
else:
    executeCode(file_source + ".gen")
    os.remove(file_source + ".gen")