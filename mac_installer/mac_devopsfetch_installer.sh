#!/bin/bash

# Ensure Homebrew is installed
if ! command -v brew &>/dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install dependencies
brew update
brew install python3 nginx docker
pip3 install psutil tabulate

# Copy devopsfetch.py to /usr/local/bin
sudo cp devopsfetch.py /usr/local/bin/devopsfetch
sudo chmod +x /usr/local/bin/devopsfetch

# Create log directory
sudo mkdir -p /usr/local/var/log/devopsfetch

# Create launchd service file
cat <<EOF | sudo tee /Library/LaunchDaemons/com.devopsfetch.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.devopsfetch</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/devopsfetch</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/usr/local/var/log/devopsfetch/devopsfetch.log</string>
    <key>StandardErrorPath</key>
    <string>/usr/local/var/log/devopsfetch/devopsfetch.log</string>
</dict>
</plist>
EOF

# Load the launchd service
sudo launchctl load /Library/LaunchDaemons/com.devopsfetch.plist
