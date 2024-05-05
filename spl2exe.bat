:: SPL2EXE

@echo off

echo spl2exe version 1.0
echo by Teo Jauffret

xcopy /y %1 SOURCE.spl

pyinstaller --onefile --name %2 --add-data "SOURCE.spl:." template.py

del SOURCE.spl