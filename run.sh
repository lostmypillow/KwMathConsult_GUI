#!/bin/bash

# Exit on error
set -e
APP_DIR="$(pwd)"

echo "SETUP [Update system]"
sudo apt update > /dev/null
sudo apt full-upgrade > /dev/null
echo "ok"

echo "SETUP [Install libxcb-cursor0]"
sudo apt-get install libxcb-cursor0 > /dev/null
echo "ok"


echo "SETUP [Configure .env file]"
ENV_FILE=".env"

nano $ENV_FILE

# Confirm the file was edited
echo "SETUP [Review the env variables]:"
cat $ENV_FILE
echo "SETUP [Ensure these environment variables are correct before proceeding.]"
read -p "Press Enter to continue or Ctrl+C to abort."

echo "SETUP [Ensure virtual environment is enabled]"
if [ ! -d "$APP_DIR/.venv" ]; then
    python3 -m venv "$APP_DIR/.venv" >/dev/null
fi
source "$APP_DIR/.venv/bin/activate"
echo "ok"

echo "SETUP [Install Python requirements]"
pip install -r "$APP_DIR/requirements.txt" >/dev/null
echo "ok"


echo "BUILD [Build executable with pyside6-deploy]"
pyside6-deploy --name kwmathconsult --mode standalone Python/main.py

# Get the .bin filename dynamically
BIN_FILE=$(find ./kwmathconsult.dist -maxdepth 1 -type f -name "*.bin" -exec basename {} \;)

if [ -n "$BIN_FILE" ]; then
    sudo chmod +x "$APP_DIR/kwmathconsult.dist/$BIN_FILE"
else
    echo "Error: No .bin file found!"
    exit 1
fi
echo "ok"

echo "DEPLOY [Create .desktop file]"
DESKTOP_FILE="$HOME/Desktop/數輔刷卡.desktop"

if [ ! -f "$DESKTOP_FILE" ]; then
    echo "Creating desktop file..." >/dev/null
    cat <<EOF >"$DESKTOP_FILE"
[Desktop Entry]
Version=0.2.0
Name=數輔刷卡
Comment=Launch KwMathConsult GUI
Exec=/bin/bash -c "cd $APP_DIR/kwmathconsult.dist && ./$BIN_FILE"
Icon=application-x-executable
Terminal=true
Type=Application
Categories=Utility;Application;
StartupNotify=true
EOF
    chmod 0755 "$DESKTOP_FILE"
fi
echo "ok"


echo "POST-INSTALL TASK [Copying .desktop file to .config/autostart]"
AUTOSTART_DIR="$HOME/.config/autostart"
if [ ! -d "$AUTOSTART_DIR" ]; then
    mkdir -p "$AUTOSTART_DIR"
    chmod 0755 "$AUTOSTART_DIR"
fi
cp "$DESKTOP_FILE" "$AUTOSTART_DIR/數輔刷卡.desktop"
chmod 0755 "$AUTOSTART_DIR/數輔刷卡.desktop"
echo "ok"

echo "POST-INSTALL TASK [Disable screen blanking via autostart]"

AUTOSTART_FILE="$HOME/.config/lxsession/LXDE-pi/autostart"
if [ ! -f "$AUTOSTART_FILE" ]; then
    mkdir -p "$HOME/.config/lxsession/LXDE-pi"
    touch "$AUTOSTART_FILE"
fi

# Disable screen saver, DPMS, and blanking
if ! grep -q "@xset s off" "$AUTOSTART_FILE"; then
    echo "@xset s off" >> "$AUTOSTART_FILE"
fi
if ! grep -q "@xset -dpms" "$AUTOSTART_FILE"; then
    echo "@xset -dpms" >> "$AUTOSTART_FILE"
fi
if ! grep -q "@xset s noblank" "$AUTOSTART_FILE"; then
    echo "@xset s noblank" >> "$AUTOSTART_FILE"
fi

# Disable xscreensaver if it's installed
if ! grep -q "@xscreensaver -no-splash" "$AUTOSTART_FILE"; then
    echo "@xscreensaver -no-splash" >> "$AUTOSTART_FILE"
fi

echo "ok"

# Reboot to apply all changes
echo "ALL SETUP FINISHED! Please reboot the system with sudo reboot"