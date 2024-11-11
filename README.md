# Reservation System GUI

## Prerequisites (For both Development and Production)
1. If running on Linux, please run the below command before creating a virtual environment
### Ubuntu/Debian/RPi OS
```bash
sudo apt-get install python3-tk python3-venv
```
### Fedora
```bash
sudo dnf install python-tkinter
```
2. Create a virtual environment using the requirements.txt in this repo
``` bash
python3 -m .venv venv
source .venv/bin/activate
pip install -r requirements.txt
```


## Development
```bash
python3 -m main
```

## Build/Production
```bash
python3 -m build
```
And the executable would be in dist/main folder as "main.exe" or just "main" on Linux

## Authors and acknowledgment
Johnny (Lost) - jmlin0101@gmail.com