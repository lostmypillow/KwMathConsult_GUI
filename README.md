# Reservation System GUI
- [Reservation System GUI](#reservation-system-gui)
  - [Development](#development)
    - [Prerequisites](#prerequisites)
      - [For VSCode users:](#for-vscode-users)
    - [Preview](#preview)
    - [Build](#build)
  - [Production](#production)
  - [Authors](#authors)



## Development
### Prerequisites
If running this repo on Linux, please run the below command **before** creating a virtual environment:

```bash
# Ubuntu/Debian/Raspbian OS
sudo apt-get install python3-tk python3-venv

# Fedora
sudo dnf install python-tkinter
```

Only after installing the above do you create a virtual environment using the requirements.txt in this repo
``` bash
python3 -m .venv venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### For VSCode users:
Ctrl + P , select `Python: Create Environment` and remember to check requirements.txt


### Preview
```bash
python3 -m main
```

### Build
```bash
python3 -m build
```


## Production
```bash
chmod +x setup.sh
sudo ./setup.sh
```
The bash script will install all necessary prerequisites, activate virtual environment, install pip requirements, build and run the executable on a countdown of 3 seconds. It will prompt for changes in the env file, namely device number and API URL, change it then if needed. 

## Authors
Johnny (Lost) - jmlin0101@gmail.com