"""
Everything to do with 'mounts' (Linux) or 'network drives' (Windows).
"""

import os
import os.path
import subprocess


def getAllMounts():
    mounts = {}
    if os.name == 'nt':
        # TODO: For windows, we need to get the 'mount points' so we can use
        # them in the same way as on Linux.

        # import win32api
        #
        # drives = win32api.GetLogicalDriveStrings()
        # drives = drives.split('\000')[:-1]
        # print drives

        ########################################################################

        # import string
        # from ctypes import windll
        #
        # def get_drives():
        #     drives = []
        #     bitmask = windll.kernel32.GetLogicalDrives()
        #     for letter in string.uppercase:
        #         if bitmask & 1:
        #             drives.append(letter)
        #         bitmask >>= 1
        #
        #     return drives
        #
        # if __name__ == '__main__':
        #     print get_drives()  # On my PC, this prints ['A', 'C', 'D', 'F', 'H']

        return mounts
    lines = subprocess.check_output(['mount', '-l']).split('\n')
    for line in lines:
        parts = line.split(' ')
        if len(parts) > 2:
            repo = parts[0]
            directory = parts[2]
            typ = parts[4]

            hostname = ''
            share = ''
            if ':' in repo:
                splt = repo.split(':')
                hostname = splt[0]
                share = splt[1]

            mounts[directory] = {
                'repo': repo,
                'hostname': hostname,
                'share': share,
                'type': typ,
            }
    return mounts


MOUNTS = getAllMounts()


def getMount(mounts, path):
    mount = None
    mount_dir = None
    keys = reversed(sorted(mounts.keys()))
    for k in keys:
        if path.startswith(k) is True:
            mount = mounts[k]
            mount_dir = k
            break
    return mount_dir, mount
