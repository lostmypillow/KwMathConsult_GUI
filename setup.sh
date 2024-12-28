#!/bin/bash

# Exit on error
set -e

if [ ! -f ~/launch.sh ]; then
    echo "Creating launch.sh in the home directory..."
    
    # Create launch.sh and add content
    echo "#!/bin/bash
cd \$(dirname \$0)
sudo ./setup.sh" > ~/launch.sh
    
    # Make it executable
    chmod +x ~/launch.sh
    echo "[STEP 0] launch.sh created and made executable."
else
    echo "[STEP 0] launch.sh already exists in the home directory."
fi


echo "[STEP 1] Updating system..."
sudo apt update

echo "[STEP 2] Ensuring python and pip are installed..."
sudo apt install -y python3-venv python3-pip

if ! fc-list | grep -i "Sarasa Fixed TC"; then
    echo "[STEP 3] Font 'Sarasa Fixed TC' not found. Installing..."

    # Download the Sarasa Fixed TC font archive
    FONT_URL="https://github.com/be5invis/Sarasa-Gothic/releases/download/v1.0.26/SarasaFixed-TTF-1.0.26.7z"
    FONT_ARCHIVE="SarasaFixed-TTF-1.0.26.7z"
    sudo apt install -y wget p7zip-full
    wget -O $FONT_ARCHIVE $FONT_URL
    7z x $FONT_ARCHIVE -oSarasaFixed
    sudo cp -r SarasaFixed/* /usr/share/fonts/
    echo "Refreshing font cache..."
    sudo fc-cache -fv
    rm -rf $FONT_ARCHIVE SarasaFixed
else
    echo "[STEP 3] Font 'Sarasa Fixed TC' is already installed."
fi

echo "[STEP 4] Creating virtual environment if one isn't created..."
if [ ! -d ".venv" ]; then 
    python3 -m venv .venv
fi

echo "[STEP 5] Activating virtual environment..."
source .venv/bin/activate


echo "[STEP 6] Installing from requirements.txt"
pip install -r requirements.txt

echo "[STEP 7] Preparing to run KwConsult in"
for i in {3..1}; do
    echo "$i..."
    sleep 1
done

python main.py