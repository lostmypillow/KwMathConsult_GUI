import subprocess
result = subprocess.run("pip show customtkinter", shell=True, capture_output=True, text=True)
output = result.stdout
customtkinter_location = str((output.split('\n')[7]).split(' ')[1]) + '/customtkinter;customtkinter/'
print(customtkinter_location)
subprocess.run([
    'pyinstaller',
    '--noconfirm',
    '--onedir',
    '--windowed',
    '--add-data',
    customtkinter_location,
    'main.py'
])
