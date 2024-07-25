import argparse
import psutil
import subprocess
import pwd
from datetime import datetime
from tabulate import tabulate

def get_active_ports():
    connections = psutil.net_connections()
    data = []
    for conn in connections:
        if conn.status == 'LISTEN':
            data.append([conn.laddr.port, conn.laddr.ip, conn.pid, psutil.Process(conn.pid).name()])
    return data

def get_detailed_port_info(port):
    connections = psutil.net_connections()
    data = []
    for conn in connections:
        if conn.laddr.port == port:
            data.append([conn.laddr.port, conn.laddr.ip, conn.pid, psutil.Process(conn.pid).name(), conn.status])
    return data

def get_docker_info():
    images = subprocess.check_output(["docker", "images", "--format", "{{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedAt}}"]).decode().splitlines()
    containers = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}\t{{.Image}}\t{{.Status}}"]).decode().splitlines()
    return images, containers

def get_detailed_container_info(container_name):
    details = subprocess.check_output(["docker", "inspect", container_name]).decode()
    return details

def get_nginx_info():
    domains = subprocess.check_output(["nginx", "-T"]).decode()
    return domains

def get_detailed_nginx_info(domain):
    config = subprocess.check_output(["nginx", "-T"]).decode()
    return config

def get_user_info():
    users = []
    for user in pwd.getpwall():
        try:
            last_login = subprocess.check_output(["lastlog", "-u", user.pw_name]).decode().splitlines()[-1].split()[-2:]
            last_login = ' '.join(last_login)
        except Exception:
            last_login = "Never logged in"
        users.append([user.pw_name, user.pw_uid, user.pw_gid, last_login])
    return users

def get_detailed_user_info(username):
    user = pwd.getpwnam(username)
    last_login = subprocess.check_output(["lastlog", "-u", username]).decode().splitlines()[-1].split()[-2:]
    last_login = ' '.join(last_login)
    return [user.pw_name, user.pw_uid, user.pw_gid, last_login]

def main():
    parser = argparse.ArgumentParser(description="DevOps Fetch Tool")
    parser.add_argument("-p", "--port", nargs='?', const='all', help="Display active ports and services or detailed information about a specific port")
    parser.add_argument("-d", "--docker", nargs='?', const='all', help="List Docker images and containers or provide detailed information about a specific container")
    parser.add_argument("-n", "--nginx", nargs='?', const='all', help="Display Nginx domains and their ports or provide detailed configuration information for a specific domain")
    parser.add_argument("-u", "--users", nargs='?', const='all', help="List users and their last login times or provide detailed information about a specific user")
    parser.add_argument("-t", "--time", help="Display activities within a specified time range")

    args = parser.parse_args()

    if args.port:
        if args.port == 'all':
            ports = get_active_ports()
            print(tabulate(ports, headers=["Port", "IP Address", "PID", "Service Name"]))
        else:
            port_info = get_detailed_port_info(int(args.port))
            print(tabulate(port_info, headers=["Port", "IP Address", "PID", "Service Name", "Status"]))

    if args.docker:
        if args.docker == 'all':
            images, containers = get_docker_info()
            print("Docker Images:")
            print(tabulate([img.split('\t') for img in images], headers=["Repository", "Tag", "Image ID", "Created At"]))
            print("\nDocker Containers:")
            print(tabulate([cont.split('\t') for cont in containers], headers=["Name", "Image", "Status"]))
        else:
            container_info = get_detailed_container_info(args.docker)
            print(container_info)

    if args.nginx:
        if args.nginx == 'all':
            nginx_info = get_nginx_info()
            print(nginx_info)
        else:
            nginx_details = get_detailed_nginx_info(args.nginx)
            print(nginx_details)

    if args.users:
        if args.users == 'all':
            users = get_user_info()
            print(tabulate(users, headers=["Username", "UID", "GID", "Last Login"]))
        else:
            user_info = get_detailed_user_info(args.users)
            print(tabulate([user_info], headers=["Username", "UID", "GID", "Last Login"]))

if __name__ == "__main__":
    main()
