import PyInstaller.__main__
import os
import sys

# Create the spec file first
PyInstaller.__main__.run([
    'main.py',
    '--name=HSN_Tax_Calculator',
    '--windowed',  # No console window
    '--onefile',   # Single executable file
    '--icon=NONE', # Replace with path to your icon if you have one
    '--add-data=HSN_SAC.xlsx;.',  # Include the Excel file
    '--add-data=.env;.',  # Include the .env file
    '--target-architecture=x86_64',  # Target 64-bit Windows
    '--clean',  # Clean PyInstaller cache
    '--noconfirm',  # Replace output directory without asking
    '--uac-admin'  # Request admin privileges (helps with compatibility)
])

print("Executable created successfully in the dist folder!")
print(f"Path: {os.path.abspath('dist/HSN_Tax_Calculator.exe')}")