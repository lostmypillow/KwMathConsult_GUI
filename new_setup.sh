#!/bin/bash

# Exit on error
set -e

echo "Updating system..."
sudo apt update

echo "Installing pipx..."
sudo apt install -y pipx

echo "Ensuring pipx is in the PATH..."
pipx ensurepath

# Source the shell configuration file to apply changes immediately
# Adjust based on your shell (e.g., .bashrc, .zshrc)
if [ -f "$HOME/.bashrc" ]; then
    echo "Sourcing .bashrc to apply pipx path changes..."
    source "$HOME/.bashrc"
elif [ -f "$HOME/.zshrc" ]; then
    echo "Sourcing .zshrc to apply pipx path changes..."
    source "$HOME/.zshrc"
else
    echo "No known shell configuration file found. You may need to manually reload your shell."
fi

echo "Installing Ansible via pipx..."
pipx install --include-deps ansible

# Ensure .env file exists
ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo "No .env file found. Creating a new one..."
    echo "# Example environment variables" > $ENV_FILE
    echo "APP_ENV=production" >> $ENV_FILE
    echo "DEBUG=false" >> $ENV_FILE
fi

echo "Opening .env file for editing..."
nano $ENV_FILE

# Confirm the file was edited
echo "Review the .env file:"
cat $ENV_FILE

echo "Ensure these environment variables are correct before proceeding."
read -p "Press Enter to continue or Ctrl+C to abort."

# Run Ansible playbook
echo "Running Ansible playbook..."
ansible-playbook -i "localhost," --connection=local kwconsultgui.yml