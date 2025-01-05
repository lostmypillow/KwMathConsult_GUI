# **Kaowei Consult GUI**
- [**Kaowei Consult GUI**](#kaowei-consult-gui)
  - [Development](#development)
    - [Prerequisites](#prerequisites)
      - [For VSCode users:](#for-vscode-users)
    - [Preview](#preview)
    - [Build](#build)
  - [Production](#production)
  - [Problems I faced \& my solutions](#problems-i-faced--my-solutions)
    - [Sub-process /usr/bin/dpkg returned error code (1) at sudo apt update in RPi](#sub-process-usrbindpkg-returned-error-code-1-at-sudo-apt-update-in-rpi)
    - [HEAD not found when you git clone this repo](#head-not-found-when-you-git-clone-this-repo)
  - [Authors](#authors)



## Development
### Prerequisites
If developing this repo on Linux, please run the below command **before** creating a virtual environment:

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
# if the RPi is outfitted with 3 inch touchscreen, run this first:
sudo chmod +x screen-setup.sh
sudo ./screen_setup.sh

# Main setup script (it will install prereqs & auto start Ansible playbook)
sudo chmod +x setup.sh
sudo ./setup.sh

# After setup script is finished
sudo reboot
```

## Problems I faced & my solutions
### Sub-process /usr/bin/dpkg returned error code (1) at sudo apt update in RPi
And if it's about something something initramfs:

1. Check the Current MODULES Setting
```bash
grep MODULES /etc/initramfs-tools/initramfs.conf
```
2. If it says dep:

    Back up the current configuration:

```bash
cp /etc/initramfs-tools/initramfs.conf /etc/initramfs-tools/initramfs.conf.bak
```

3. Edit the file:

```bash
sudo nano /etc/initramfs-tools/initramfs.conf
```

4. Change `MODULES=dep` to `MODULES=most`

5. Update initramfs for your current kernel:
```bash
sudo update-initramfs -u
```
6. Reboot
```bash
sudo reboot
```
### HEAD not found when you git clone this repo
1. `cd` into the repo
2. `git checkout main`

## Authors
Johnny (Lost) - jmlin0101@gmail.com