#!/bin/bash

# Update package list and upgrade all packages
sudo apt-get update
sudo apt-get upgrade -y

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install necessary dependencies
sudo apt-get install -y python3 python3-venv nginx containerd.io

# Create and activate virtual environment
python3 -m venv devopsfetch-venv
source devopsfetch-venv/bin/activate

# Install Python packages
pip install psutil tabulate

# Copy devopsfetch.py to /usr/local/bin
sudo cp devopsfetch.py /usr/local/bin/devopsfetch
sudo chmod +x /usr/local/bin/devopsfetch

# Create log directory
sudo mkdir -p /var/log/devopsfetch

# Create systemd service file
sudo bash -c 'cat <<EOF > /etc/systemd/system/devopsfetch.service
[Unit]
Description=DevOpsFetch Service
After=network.target

[Service]
ExecStart=/usr/local/bin/devopsfetch
StandardOutput=append:/var/log/devopsfetch/devopsfetch.log
StandardError=append:/var/log/devopsfetch/devopsfetch.log
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF'

# Reload systemd and enable the service
sudo systemctl daemon-reload
sudo systemctl enable devopsfetch.service
sudo systemctl start devopsfetch.service

# Create logrotate configuration
sudo bash -c 'cat <<EOF > /etc/logrotate.d/devopsfetch
/var/log/devopsfetch/devopsfetch.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 root utmp
    sharedscripts
    postrotate
        systemctl reload devopsfetch > /dev/null 2>&1 || true
    endscript
}
EOF'
