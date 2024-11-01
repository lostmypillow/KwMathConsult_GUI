import subprocess

subprocess.run([
    'pyinstaller',
    '--noconfirm',
    '--onedir',
    '--windowed',
    '--add-data',
    '.venv/Lib/site-packages/customtkinter;customtkinter/',
    'main.py'
])
