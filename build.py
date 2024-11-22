import subprocess
import sys
import os
import shutil
location_string = 'images/*:images' if sys.platform.startswith(
    'linux') else 'images/*;images'
subprocess.run([
    'pyinstaller', '--noconfirm', '--onefile', '--windowed',
    '--hidden-import=PIL._tkinter_finder',
    '--collect-data', 'sv_ttk',
    '--add-data', location_string,
    'main.py'
])
if os.path.exists('.env'):
    try:
        shutil.copy('.env', 'dist')
        print(f'Copied env file')
        shutil.copytree('./images', 'dist/images', dirs_exist_ok=True)
        print('Copied images folder')
    except Exception as e:
        print(f"Error copying files: {e}")
else:
    print(".env file not found.")
print('Build Complete.')
