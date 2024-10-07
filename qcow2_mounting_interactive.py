#!/usr/bin/env python3
# File name: qcow2_mounting.py
# Description: Basic script for mounting qcow2 files
# Author: Artur Glogowski
# Date: 04-10-2024
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
    # Define the new mount point
    mount_point = '/vm_disc'

    # Create the mount point directory
    create_mount_point(mount_point)

    while True:
        print('Do you want to (m)ount or (u)mount the qcow2 image? Or (e)xit.')
        usage = input().lower()

        if usage == 'm':
            print('Loading the nbd module.')
            modprobe('nbd')
            
            print('What is the location and name of the qcow2 file to mount?')
            location = input().strip()
            
            print(f'Connecting the {location} image to a network block device.')
            connect = ['sudo', 'qemu-nbd', '--connect=/dev/nbd0', location]
            run_command(connect)
            
            sleep(1)
            print(f'Mounting the partition from the VM to {mount_point}.')
            mount_partition('/dev/nbd0p4', mount_point)
            print('Done.')
            sys.exit()

        elif usage == 'u':
            print('Unmounting the partition.')
            umount_partition(mount_point)
            
            print('Disconnecting the image from the network block device.')
            disconnect = ['sudo', 'qemu-nbd', '--disconnect', '/dev/nbd0']
            run_command(disconnect)
            
            print('Done.')
            sys.exit()

        elif usage == 'e':
            print('Exiting the script.')
            sys.exit()

        else:
            print('Choose the action you want to take.')

if __name__ == '__main__':
    main()

