#!/usr/bin/env python3

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
