#!/bin/bash

RED='\033[7;31m'
NC='\033[0m' # No Color

# Exit on error
set -e

echo -e "${RED}[STEP 1]${NC} Updating system..."
sudo apt update

echo -e "${RED}[STEP 2]${NC} Ensuring python, pip and tk are installed..."
sudo apt install -y python3-venv python3-pip python3-tk


if ! fc-list | grep -i "Sarasa Fixed TC"; then
    echo -e "${RED}[STEP 3]${NC} Font 'Sarasa Fixed TC' not found. Installing..."

    
    FONT_URL="https://github.com/be5invis/Sarasa-Gothic/releases/download/v1.0.26/SarasaFixed-TTF-1.0.26.7z"
    FONT_ARCHIVE="SarasaFixed-TTF-1.0.26.7z"
    sudo apt update
    sudo apt install -y wget p7zip-full
    wget -O $FONT_ARCHIVE $FONT_URL
    7z x $FONT_ARCHIVE -oSarasaFixed
    sudo cp -r SarasaFixed/* /usr/share/fonts/
    sudo fc-cache -fv
    rm -rf $FONT_ARCHIVE SarasaFixed
else
    echo -e "${RED}[STEP 3]${NC} Font 'Sarasa Fixed TC' is already installed."
fi


if [ ! -d ".venv" ]; then
    echo -e "${RED}[STEP 4]${NC} Virtual environment not found. Creating one now..."
    python3 -m venv .venv
    source .venv/bin/activate
else
    echo -e "${RED}[STEP 4]${NC} Activating virtual environment..."
    source .venv/bin/activate
fi


echo -e "${RED}[STEP 5]${NC} Installing pip requirements"
pip install -r requirements.txt


echo -e "${RED}[STEP 6]${NC} Building executable..."
pyinstaller --noconfirm --onefile --windowed \
    --hidden-import=PIL._tkinter_finder \
    --collect-data sv_ttk \
    --add-data "images/*:images" main.py
cp -r ./images dist/images
cp .env dist/


# 4. Check and modify .env file in /dist
echo -e "${RED}[STEP 7]${NC} Configuring .env file..."

cd dist

echo -e "${RED}[CONFIGURE]${NC} Current DEVICE_NUM value: $(grep 'DEVICE_NUM' .env | cut -d '=' -f2)"
read -p "Enter new DEVICE_NUM (press Enter to keep current value): " NEW_DEVICE_NUM
if [ -n "$NEW_DEVICE_NUM" ]; then
    sed -i "s/^DEVICE_NUM=.*/DEVICE_NUM=$NEW_DEVICE_NUM/" .env
    echo "${RED}Updated DEVICE_NUM to $NEW_DEVICE_NUM."
fi

echo -e "${RED}[CONFIGURE]${NC} Current API_URL value: $(grep 'API_URL' .env | cut -d '=' -f2)"
read -p "Enter new API_URL (press Enter to keep current value): " NEW_API_URL
if [ -n "$NEW_API_URL" ]; then
    sed -i "s|^API_URL=.*|API_URL=$NEW_API_URL|" .env
    echo "Updated API_URL to $NEW_API_URL."
fi



SERVICE_FILE="/etc/systemd/system/kwconsult.service"
if [ -f "$SERVICE_FILE" ]; then
    echo -e "${RED}[WARNING]${NC} Existing service found. Stopping and removing it..."
    sudo systemctl stop main.service
    sudo systemctl disable main.service
    sudo rm -f "$SERVICE_FILE"
fi

echo -e "${RED}[STEP 8]${NC} Creating new systemd service kwconsult..."
sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=KwConsult GUT
After=network.target

[Service]
Type=simple
ExecStart=$(pwd)/main
Restart=on-failure
User=$(whoami)
WorkingDirectory=$(pwd)

[Install]
WantedBy=multi-user.target
EOF

echo -e "${RED}[STEP 9]${NC} Reloading systemd daemon..."
sudo systemctl daemon-reload

echo -e "${RED}[STEP 10]${NC} Enabling and starting the service in 5 seconds..."
for i in {5..1}; do
    echo "$i..."
    sleep 1
done

sudo systemctl enable kwconsult.service
sudo systemctl start kwconsult.service