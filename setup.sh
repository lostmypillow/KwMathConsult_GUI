#!/bin/bash

# Exit on error
set -e

echo "SETUP [Update system]"
sudo apt update > /dev/null
echo "ok: System updated"

echo "SETUP [Ensure Ansible is installed (might take a while, be patient)]"
if ! command -v pipx &> /dev/null; then
    sudo apt install -y pipx > /dev/null
fi
pipx ensurepath

if [ -f "$HOME/.bashrc" ]; then
    source "$HOME/.bashrc"
fi

if ! pipx list | grep -q ansible; then
    pipx install --include-deps ansible > /dev/null
fi
echo "ok: ansible is installed"

echo "SETUP [Configure .env file]"
ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo "DEVICE_NUM=1" >> $ENV_FILE
    echo "API_URL=http://192.168.2.6:8001" >> $ENV_FILE
fi

nano $ENV_FILE

# Confirm the file was edited
echo "Review the env variables:"
cat $ENV_FILE
echo "Ensure these environment variables are correct before proceeding."
read -p "Press Enter to continue or Ctrl+C to abort."

PLAYBOOK_FILE="kwconsultgui.ansible.yml"

if [ -f "$PLAYBOOK_FILE" ]; then
    echo "SETUP [Run Ansible playbook]"
    ansible-playbook -i "localhost," --connection=local $PLAYBOOK_FILE
else
    echo "ERROR [Playbook file $PLAYBOOK_FILE not found. Exiting.]"
    exit 1
fi

echo "POST-INSTALL TASK [Disable screen blanking via autostart]"


AUTOSTART_FILE="/home/pi/.config/lxsession/LXDE-pi/autostart"
if [ ! -f "$AUTOSTART_FILE" ]; then
    mkdir -p /home/pi/.config/lxsession/LXDE-pi
    touch $AUTOSTART_FILE
fi

if ! grep -q "@xset -dpms" "$AUTOSTART_FILE"; then
    echo "@xset -dpms" >> "$AUTOSTART_FILE"
fi

if ! grep -q "@xset s off" "$AUTOSTART_FILE"; then
    echo "@xset s off" >> "$AUTOSTART_FILE"
fi

echo "ok: Screen blanking and power-saving disabled via autostart file."

# Reboot to apply all changes
echo "ALL SETUP FINISHED! Please reboot the system with sudo reboot"