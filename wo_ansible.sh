#!/bin/bash

# Exit on error
set -e
APP_DIR="$(pwd)"


echo "SETUP [Update system]"
sudo apt update -qq >/dev/null
echo "ok"

echo "SETUP [Ensure necessary packages are installed]"
sudo apt-get install -y python3-venv python3-pip python3-tk wget p7zip-full >/dev/null
echo "ok"


echo "SETUP [Ensure virtual environment is enabled]"
if [ ! -d "$APP_DIR/.venv" ]; then
    python3 -m venv "$APP_DIR/.venv" >/dev/null
fi
source "$APP_DIR/.venv/bin/activate"
echo "ok"

echo "SETUP [Install Python requirements]"
pip install -r "$APP_DIR/requirements.txt" >/dev/null
echo "ok"

echo "SETUP [Build executable]"
python build.py >/dev/null
echo "ok"

echo "SETUP [Ensure Sarasa Fixed TC is installed]"
FONT_URL="https://github.com/be5invis/Sarasa-Gothic/releases/download/v1.0.26/SarasaFixed-TTF-1.0.26.7z"
FONT_ARCHIVE="/tmp/SarasaFixed-TTF-1.0.26.7z"
if ! fc-list | grep -q "Sarasa Fixed TC"; then
    wget -q "$FONT_URL" -O "$FONT_ARCHIVE" >/dev/null
    7z x "$FONT_ARCHIVE" -o/tmp/SarasaFixed >/dev/null
    sudo cp -r /tmp/SarasaFixed/* /usr/share/fonts/ >/dev/null
    fc-cache -fv >/dev/null
    rm -f "$FONT_ARCHIVE"
fi
echo "ok"

echo "SETUP [Create .desktop file]"
DESKTOP_FILE="/home/kaowei/Desktop/數輔.desktop"
if [ ! -f "$DESKTOP_FILE" ]; then
    echo "Creating desktop file..." >/dev/null
    cat <<EOF >"$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Name=數輔
Comment=Launch KwConsult GUI Application
Exec=/bin/bash -c "cd $APP_DIR/dist && ./main"
Icon=application-x-executable
Terminal=false
Type=Application
Categories=Utility;Application;
StartupNotify=true
EOF
    chmod 0755 "$DESKTOP_FILE"
fi
echo "ok"

echo "SETUP [Copying .desktop file to .config/autostart]"
AUTOSTART_DIR="/home/kaowei/.config/autostart"
if [ ! -d "$AUTOSTART_DIR" ]; then
    mkdir -p "$AUTOSTART_DIR"
    chmod 0755 "$AUTOSTART_DIR"
fi
cp "$DESKTOP_FILE" "$AUTOSTART_DIR/數輔.desktop"
chmod 0755 "$AUTOSTART_DIR/數輔.desktop"
echo "ok"


echo "SETUP [Disable screen blanking]"
AUTOSTART_FILE="/home/pi/.config/lxsession/LXDE-pi/autostart"
if [ ! -f "$AUTOSTART_FILE" ]; then
    mkdir -p /home/pi/.config/lxsession/LXDE-pi
    touch "$AUTOSTART_FILE"
fi

if ! grep -q "@xset -dpms" "$AUTOSTART_FILE"; then
    echo "@xset -dpms" >> "$AUTOSTART_FILE"
fi

if ! grep -q "@xset s off" "$AUTOSTART_FILE"; then
    echo "@xset s off" >> "$AUTOSTART_FILE"
fi
echo "ok"

echo "ALL SETUP FINISHED! Please reboot the system"
