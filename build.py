import subprocess
import sys
import os
import shutil
result = subprocess.run("pip show customtkinter",
                        shell=True, capture_output=True, text=True)
output = result.stdout
location_string = '/customtkinter:customtkinter/' if sys.platform.startswith(
    'linux') else '/customtkinter;customtkinter/'
customtkinter_location = str(
    (output.split('\n')[7]).split(' ')[1]) + location_string
subprocess.run([
    'pyinstaller', '--noconfirm', '--onedir', '--windowed',
    '--add-data', customtkinter_location, 'main.py'
])
print('Executable "main" created in dist/main')
source_env_file = '.env'
target_folder = 'dist/main'
if os.path.exists(source_env_file):
    try:
        shutil.copy(source_env_file, target_folder)
        print(f'.env file copied to {target_folder}')
        print('Build Complete. Note that entire main folder is the application, not just the executable')
    except Exception as e:
        print(f"Error copying .env file: {e}")
else:
    print(".env file not found.")
