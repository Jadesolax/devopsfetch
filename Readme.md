DevOpsFetch is a DevOps tool to collect and display system information. It provides detailed insights into active ports, user logins, Docker images,container statuses and  Nginx configurations. The tool also supports continuous monitoring and logging using a systemd service on Linux or launchd on macOS.


Installation
On Linux

git clone https://github.com/jadesolax/devopsfetch.git
cd devopsfetch
sudo ./install_devopsfetch.sh

On macOS
copy or cut mac_devopsfetch_installer.sh in the mac_installer directory to the root directory

sudo ./mac_devopsfetch_installer.sh

Usage

devopsfetch --help
Examples
Display all active ports and services:


devopsfetch -p
Detailed information about a specific port:


devopsfetch -p 80
List all Docker images and containers:


devopsfetch -d
Detailed information about a specific container:


devopsfetch -d container_name
Display all Nginx domains and their ports:


devopsfetch -n
Detailed configuration information for a specific domain:


devopsfetch -n example.com
List all users and their last login times:


devopsfetch -u
Detailed information about a specific user:


devopsfetch -u username
Logging
DevOpsFetch is configured to run as a service, continuously monitoring and logging activities to a log file. Logs can be found in:

Linux: /var/log/devopsfetch/devopsfetch.log
macOS: /usr/local/var/log/devopsfetch/devopsfetch.log

Contributing
Contributions are welcome! Please open an issue or submit a pull request to contribute.

My socials:
x.com @rocksolidly
LinkedIn https://www.linkedin.com/in/oluwole-ogunrinde-b7bb19111/

