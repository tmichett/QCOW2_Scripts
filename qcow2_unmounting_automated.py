#!/usr/bin/env python3
# File name: qcow2_unmounting.py
# Description: Script for unmounting qcow2 files non-interactively
# Author: Travis Michette
# Date: 10-04-2024

import sys
import subprocess

def run_command(command):
    """Run a command using subprocess.run and check for errors."""
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        print(f"Error: Command {' '.join(command)} failed with return code {result.returncode}")
        sys.exit(result.returncode)

def umount_partition(mount_point):
    """Unmount the specified mount point."""
    run_command(['sudo', 'umount', mount_point])

def main():
    # Define the mount point and nbd device
    mount_point = '/vm_disc'
    nbd_device = '/dev/nbd0'

    print('Unmounting the partition.')
    umount_partition(mount_point)

    print('Disconnecting the image from the network block device.')
    disconnect = ['sudo', 'qemu-nbd', '--disconnect', nbd_device]
    run_command(disconnect)

    print('Done.')

if __name__ == '__main__':
    main()
