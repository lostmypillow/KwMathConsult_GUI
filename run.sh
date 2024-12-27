#!/bin/bash

RED='\033[0;31m'
NC='\033[0m' # No Color

# Exit on error
set -e

echo -e "${RED}[SETUP 1 / 10]${NC} Updating system..."
sudo apt update

echo -e "${RED}[SETUP 2 / 10]${NC} Ensuring python, pip and tk are installed..."
sudo apt install -y python3-venv python3-pip python3-tk


if [ ! -d ".venv" ]; then
    echo -e "${RED}[SETUP 3 / 10]${NC} Creating virtual environment..."
    python3 -m venv .venv
fi

echo -e "${RED}[SETUP 4 / 10]${NC} Activating virtual environment..."
source .venv/bin/activate

echo -e "${RED}[SETUP 5 / 10]${NC} Checking for Sarasa font in this system..."

if ! fc-list | grep -i "Sarasa Fixed TC"; then
    echo -e "${RED}[SETUP 5.1 / 10]${NC} Font 'Sarasa Fixed TC' not found. Installing..."

    
    FONT_URL="https://github.com/be5invis/Sarasa-Gothic/releases/download/v1.0.26/SarasaFixed-TTF-1.0.26.7z"
    FONT_ARCHIVE="SarasaFixed-TTF-1.0.26.7z"
    
    echo -e "${RED}[SETUP 5.2 / 10]${NC} Installing p7zip to unzip the 7z file we're gonna download..."
    sudo apt update
    sudo apt install -y wget p7zip-full

    echo -e "${RED}[SETUP 5.3 / 10]${NC} Downloading Sarasa Fixed TC 7z file from GitHub..."
    wget -O $FONT_ARCHIVE $FONT_URL

    echo -e "${RED}[SETUP 5.4 / 10]${NC} Extracting Sarasa Fixed TC 7z file from GitHub..."
    7z x $FONT_ARCHIVE -oSarasaFixed

    echo -e "${RED}[SETUP 5.5 / 10]${NC} Installing Sarasa Fixed TC font..."
    sudo cp -r SarasaFixed/* /usr/share/fonts/

    # Refresh the font cache
    echo -e "${RED}[SETUP 5.6 / 10]${NC} Refreshing font cache..."
    sudo fc-cache -fv

    # Clean up the downloaded archive and extracted files
    rm -rf $FONT_ARCHIVE SarasaFixed

    echo -e "${RED}[SETUP 5.2 / 10]${NC} 'Sarasa Fixed TC' font installed successfully."
else
    echo -e "${RED}[SETUP 5.1 / 10]${NC} Font 'Sarasa Fixed TC' is already installed."
fi

echo -e "${RED}[SETUP 6 / 10]${NC} Installing pip requirements"
pip install -r requirements.txt

# 3. Run python -m build
echo -e "${RED}[SETUP 7 / 10]${NC} Building executable..."
python -m build

# 4. Check and modify .env file in /dist
echo -e "${RED}[SETUP 8 / 10]${NC} Configuring .env file..."
cd dist

# Prompt user to confirm or modify values in .env file
echo -e "${RED}[SETUP 8.1 / 10]${NC} Current DEVICE_NUM value: $(grep 'DEVICE_NUM' .env | cut -d '=' -f2)"
read -p "Enter new DEVICE_NUM (press Enter to keep current value): " NEW_DEVICE_NUM
if [ -n "$NEW_DEVICE_NUM" ]; then
    sed -i "s/^DEVICE_NUM=.*/DEVICE_NUM=$NEW_DEVICE_NUM/" .env
    echo "${RED}Updated DEVICE_NUM to $NEW_DEVICE_NUM."
fi

echo -e "${RED}[SETUP 8.2 / 10]${NC} Current API_URL value: $(grep 'API_URL' .env | cut -d '=' -f2)"
read -p "Enter new API_URL (press Enter to keep current value): " NEW_API_URL
if [ -n "$NEW_API_URL" ]; then
    sed -i "s|^API_URL=.*|API_URL=$NEW_API_URL|" .env
    echo "Updated API_URL to $NEW_API_URL."
fi

# 5. Countdown before running ./main
echo -e "${RED}[SETUP 9 / 10]${NC} Setup complete. Preparing to run executable in"
for i in {5..1}; do
    echo "$i..."
    sleep 1
done

# Run ./main (assuming it's an executable or script)
echo -e "${RED}[SETUP 10 / 10]${NC} Running ./main..."
./main