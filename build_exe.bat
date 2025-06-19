@echo off
echo Building HSN Tax Calculator executable...
pyinstaller --onefile --windowed --icon=NONE --add-data "HSN_SAC.xlsx;." --add-data ".env;." --name "HSN_Tax_Calculator" main.py
echo Build complete! Executable is in the dist folder.
pause