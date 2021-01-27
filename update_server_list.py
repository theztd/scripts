#!/usr/bin/env python3
# Simple python SSH example with ed25519 key encryted by password
# - this script get csv list of servers and for each server get OS version and append it to list
# - before start define env variables SSH_KEY_PATH and SSH_KEY_PASSWORD
# - the script use values from hostname collumn to connect to server and do it as user root, 
#   the both are easy changable in code below.
#
# Example  this_command.py input_file.csv output_file.csv


import paramiko
import os
from sys import argv
import csv

INF=argv[1]
OUTF=argv[2]
SSH_KEY_PATH=os.getenv("SSH_KEY_PATH")
SSH_KEY_PASSWORD=os.getenv("SSH_KEY_PASSWORD")


def ssh(host, user, cmd):
    key = paramiko.ed25519key.Ed25519Key(
                                filename=SSH_KEY_PATH, 
                                password=SSH_KEY_PASSWORD
                            )
    _ssh = paramiko.SSHClient()
    # Known_hosts solution
    _ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    _ssh.connect(hostname=host, username=user, pkey = key)
    # Run the command and save outputs
    stdin, stdout, stderr = _ssh.exec_command(cmd)
    
    # Return nice utf-8 output
    return stdout.read().decode('utf-8').strip()


if __name__ == "__main__":
    out = []
    with open(INF) as F:
        reader = csv.DictReader(F)
        for l in reader:
            try:
                ver = ssh(l["hostname"], "root", "cat /etc/debian_version")
                l["os_ver"] = ver
                out.append(l)

            except:
                print("ERR:   ", l)
    
    # Get list of coll names
    fields = out[1].keys()

    # Generate output csv file
    with open(OUTF, "w") as FOUT:
        writer = csv.DictWriter(FOUT, fieldnames=fields)
        writer.writeheader()
        for l in out:
            writer.writerow(l)

