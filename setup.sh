#!/bin/bash

# Set up environment for Notepad Automation Bot
echo "Setting up environment for Notepad Automation Bot..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment
echo -e "\n1. Creating virtual environment..."
python3 -m venv notepad_bot_env

# Determine OS for activation commands
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    ACTIVATE_CMD="notepad_bot_env\\Scripts\\activate"
    PYTHON_CMD="notepad_bot_env\\Scripts\\python.exe"
    PIP_CMD="notepad_bot_env\\Scripts\\pip.exe"
else
    # Unix-like (Linux, macOS)
    ACTIVATE_CMD="source notepad_bot_env/bin/activate"
    PYTHON_CMD="notepad_bot_env/bin/python"
    PIP_CMD="notepad_bot_env/bin/pip"
fi

# Activate virtual environment
echo -e "\n2. Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source notepad_bot_env/Scripts/activate
else
    source notepad_bot_env/bin/activate
fi

# Upgrade pip
echo -e "\n3. Upgrading pip..."
python -m pip install --upgrade pip

# Install required packages
echo -e "\n4. Installing required packages..."
pip install botcity-core botcity-desktop pyautogui requests

# Create project directory on desktop
echo -e "\n5. Creating project directory on desktop..."
DESKTOP_PATH="$HOME/Desktop/tjm-project"
mkdir -p "$DESKTOP_PATH"
echo "Directory created at: $DESKTOP_PATH"

# Create a simple activation script for later use
echo -e "\n6. Creating activation script..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "@echo off" > activate_env.bat
    echo "call notepad_bot_env\\Scripts\\activate" >> activate_env.bat
    echo "echo Environment activated! You can now run: python notepad_bot.py" >> activate_env.bat
    echo "Activation script created: activate_env.bat"
else
    echo "#!/bin/bash" > activate_env.sh
    echo "source notepad_bot_env/bin/activate" >> activate_env.sh
    echo "echo Environment activated! You can now run: python notepad_bot.py" >> activate_env.sh
    chmod +x activate_env.sh
    echo "Activation script created: activate_env.sh"
fi

echo -e "\nSetup complete! You can now run the bot script."
echo -e "\nTo activate the virtual environment in the future:"
echo "    $ACTIVATE_CMD"
echo -e "\nOr use the activation script created for convenience."