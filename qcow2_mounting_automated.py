#!/usr/bin/env python3
# File name: qcow2_mounting.py
# Description: Script for mounting qcow2 files non-interactively
# Original Author: Artur Glogowski
# Modification Author: Travis Michette
# Date: 10-04-2024

import sys
import subprocess
import os
from time import sleep

def run_command(command):
    """Run a command using subprocess.run and check for errors."""
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        print(f"Error: Command {' '.join(command)} failed with return code {result.returncode}")
        sys.exit(result.returncode)

def create_mount_point(mount_point):
    """Create the mount point if it doesn't exist."""
    if not os.path.exists(mount_point):
        print(f"Creating mount point at {mount_point}.")
        run_command(['sudo', 'mkdir', '-p', mount_point])

def modprobe(module):
    """Load a kernel module."""
    run_command(['sudo', 'modprobe', module])

def rmmod(module):
    """Unload a kernel module."""
    run_command(['sudo', 'rmmod', module])

def mount_partition(device, mount_point):
    """Mount a device to the specified mount point."""
    run_command(['sudo', 'mount', device, mount_point])

def umount_partition(mount_point):
    """Unmount the specified mount point."""
    run_command(['sudo', 'umount', mount_point])

def main():
    # Check if a filename is provided
    if len(sys.argv) != 2:
        print("Usage: qcow2_mounting.py <qcow2_file>")
        sys.exit(1)

    # Define the new mount point
    mount_point = '/vm_disc'

    # QCOW2 file path from command-line argument
    qcow2_file = sys.argv[1]

    # Ensure the file exists
    if not os.path.isfile(qcow2_file):
        print(f"Error: QCOW2 file '{qcow2_file}' not found.")
        sys.exit(1)

    # Create the mount point directory
    create_mount_point(mount_point)

    print('Loading the nbd module.')
    modprobe('nbd')
    
    print(f'Connecting the {qcow2_file} image to a network block device.')
    connect = ['sudo', 'qemu-nbd', '--connect=/dev/nbd0', qcow2_file]
    run_command(connect)
    
    sleep(1)
    
    print(f'Mounting the partition from the VM to {mount_point}.')
    mount_partition('/dev/nbd0p4', mount_point)  # Hardcoded partition, can be made dynamic
    print('Done.')

if __name__ == '__main__':
    main()
