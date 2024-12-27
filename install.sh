#!/bin/bash

# Exit on error
set -e

echo "[SETUP 1 / 10] Updating system..."
sudo apt update

echo "[SETUP 2 / 10] Ensuring python and pip are installed..."
sudo apt install -y python3-venv python3-pip



# 1. Create and activate virtual environment
if [ ! -d ".venv" ]; then
    echo "[SETUP 3 / 10] Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate the virtual environment
echo "[SETUP 4 / 10] Activating virtual environment..."
source .venv/bin/activate

echo "[SETUP 5 / 10] Checking for Sarasa font in this system..."
# 2. Check if 'Sarasa Fixed TC' font is installed
if ! fc-list | grep -i "Sarasa Fixed TC"; then
    echo "[SETUP 5.1 / 9] Font 'Sarasa Fixed TC' not found. Installing..."

    # Download the Sarasa Fixed TC font archive
    FONT_URL="https://github.com/be5invis/Sarasa-Gothic/releases/download/v1.0.26/SarasaFixed-TTF-1.0.26.7z"
    FONT_ARCHIVE="SarasaFixed-TTF-1.0.26.7z"
    
    # Install necessary utilities to download and extract the font
    sudo apt update
    sudo apt install -y wget p7zip-full

    # Download the font archive
    wget -O $FONT_ARCHIVE $FONT_URL

    # Extract the archive
    7z x $FONT_ARCHIVE -oSarasaFixed

    # Install the font by copying to /usr/share/fonts
    sudo cp -r SarasaFixed/* /usr/share/fonts/

    # Refresh the font cache
    echo "Refreshing font cache..."
    sudo fc-cache -fv

    # Clean up the downloaded archive and extracted files
    rm -rf $FONT_ARCHIVE SarasaFixed

    echo "[SETUP 5.2 / 10] 'Sarasa Fixed TC' font installed successfully."
else
    echo "[SETUP 5.1 / 10] Font 'Sarasa Fixed TC' is already installed."
fi

echo "[SETUP 6 / 10] Installing from requireemnts.txt"
pip install -r requirements.txt

# 3. Run python -m build
echo "[SETUP 7 / 10] Building executable..."
python -m build

# 4. Check and modify .env file in /dist
echo "[SETUP 8 / 10] Setting up .env file..."
cd dist

# Check if .env file exists, create if it doesn't
if [ ! -f ".env" ]; then
    echo "[SETUP 7.1 / 10] .env file not found, creating one..."
    echo "DEVICE_NUM=1" > .env
    echo "API_URL=http://192.168.2.6:8001" >> .env
fi

# Prompt user to confirm or modify values in .env file
echo "Current DEVICE_NUM value: $(grep 'DEVICE_NUM' .env | cut -d '=' -f2)"
read -p "Enter new DEVICE_NUM (press Enter to keep current value): " NEW_DEVICE_NUM
if [ -n "$NEW_DEVICE_NUM" ]; then
    sed -i "s/^DEVICE_NUM=.*/DEVICE_NUM=$NEW_DEVICE_NUM/" .env
    echo "Updated DEVICE_NUM to $NEW_DEVICE_NUM."
fi

echo "Current API_URL value: $(grep 'API_URL' .env | cut -d '=' -f2)"
read -p "Enter new API_URL (press Enter to keep current value): " NEW_API_URL
if [ -n "$NEW_API_URL" ]; then
    sed -i "s|^API_URL=.*|API_URL=$NEW_API_URL|" .env
    echo "Updated API_URL to $NEW_API_URL."
fi

# 5. Countdown before running ./main
echo "[SETUP 9 / 10] Preparing to run executable in"
for i in {3..1}; do
    echo "$i..."
    sleep 1
done

# Run ./main (assuming it's an executable or script)
echo "[SETUP 10 / 10] Running ./main..."
./main