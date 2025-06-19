@echo off
echo Creating distribution package...

:: Create distribution directory
mkdir dist_package
copy dist\HSN_Tax_Calculator.exe dist_package\
copy README.txt dist_package\

echo Distribution package created in dist_package folder.
echo You can now zip this folder and distribute it.
pause