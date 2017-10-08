"""
File Data database tables
"""

import os
import os.path
import sys
import subprocess
import mimetypes
import re
import time

from sqlalchemy import (
    Column, Integer, BigInteger, String, Boolean, ForeignKey
)
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

import mediaDB2.config as config
import mediaDB2.setup as setup
import mediaDB2.models.modelbase as base
import mediaDB2.models.path
import mediaDB2.models.mixins as mixins
from mediaDB2.models import *


# initialise mimetypes with user-defined values.
mime_files = config.getMimeFilePaths()
mimetypes.init(mime_files)

SPLIT_CHARS = config.getSplitChars()
UNNEEDED_WORDS = config.getExcludedWords()


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
    for d in keys:
        if path.startswith(d) is True:
            mount = mounts[d]
            mount_dir = d
            break
    return mount_dir, mount


def createRepo(session, mount):
    hostname = mount['hostname']
    share = mount['share']

    q = session.query(Repository)
    q = q.filter(Repository.host_name == hostname, Repository.share_name == share)
    repo = q.first()

    if repo is None:
        repo = Repository(host_name=hostname, share_name=share)
        session.add(repo)
    return repo


def createTags(path, file_ext):
    split = path.strip()

    for char in SPLIT_CHARS:
        split = split.replace(char, ' ').strip()
    tags = []
    tmp = re.split(r'([A-Z]+[a-z]*)', split)
    for tag in tmp:
        tag = tag.strip()
        if len(tag):
            if tag not in tags:
                tags.append(tag)
            dashSplit = tag.split('-')
            if len(dashSplit) > 1:
                for t in dashSplit:
                    if t not in tags:
                        tags.append(t)
    the_tags = []
    for tag in tags:
        tag = tag.lower()
        if len(tag) <= 1:
            continue
        if not tag.isalpha():
            continue
        if tag in UNNEEDED_WORDS:
            continue
        if tag == file_ext:
            continue
        if tag not in the_tags:
            the_tags.append(tag)
    return the_tags


def createMime(session, path):
    mime_obj = None

    mime = mimetypes.guess_type(path, strict=False)
    if mime and len(mime) == 2 and mime[0]:
        tmp = str(mime[0]).split('/')
        type_name = tmp[0]
        subtype_name = tmp[1]

        # Query Mime
        q_mime = session.query(Mime).join(MimeType, MimeSubtype)
        q_mime = q_mime.filter(MimeType.name == type_name,
                               MimeSubtype.name == subtype_name)
        mime_obj = q_mime.first()
        if mime_obj is None:
            # Mime Type
            q_type = session.query(MimeType)
            q_type = q_type.filter(MimeType.name == type_name)
            mime_type = q_type.first()
            if mime_type is None:
                mime_type = MimeType(name=type_name)
                session.add(mime_type)

            # Mime Sub-type
            q_subtype = session.query(MimeSubtype)
            q_subtype = q_subtype.filter(MimeSubtype.name == subtype_name)
            mime_subtype = q_subtype.first()
            if mime_subtype is None:
                mime_subtype = MimeSubtype(name=subtype_name)
                session.add(mime_subtype)

            # Mime Object
            mime_obj = Mime(
                mime_type=mime_type,
                mime_subtype=mime_subtype
            )
            session.add(mime_obj)

    return mime_obj


def addPath(session, full_path, parent_path):
    # Repository
    repository = None
    mount_dir, mount = getMount(MOUNTS, full_path)
    if mount:
        repository = createRepo(session, mount)
    session.add(repository)

    # Get the final end_path
    end_path = full_path[len(mount_dir):]
    end_path = end_path.encode('ascii', errors='ignore')
    if len(end_path.strip()) == 0:
        return None

    # Query an existing Path
    q = session.query(Path)
    q = q.filter(Path.path == end_path)
    p = q.first()

    # Path
    extension = None
    if os.path.isdir(full_path):
        if p is None:
            p = Path(path=end_path)
        p.is_file = False
        p.file_size = None
        p.mime = None

    elif os.path.isfile(full_path):
        # Size
        size = 0
        try:
            size = os.path.getsize(full_path)
        except OSError:
            pass

        # MIME type
        mime = createMime(session, full_path)

        # Path
        if p is None:
            p = Path(path=end_path)
        p.is_file = True
        p.file_size = size
        p.mime = mime

        # File Extension
        n, ext = os.path.splitext(full_path)
        extension = ext[1:].lower()

    # Parent directory
    if parent_path is not None:
        p.parent = parent_path

    # Repository
    p.repository = repository

    # Tags
    # NOTE: Only use file name for tags.
    dir_path, file_name = os.path.split(full_path)
    tag_names = createTags(file_name, extension)
    for name in tag_names:
        tag = session.query(Tag).filter_by(name=name).first()
        if tag is None:
            tag = Tag(name=name)
            session.add(tag)

        pt = session.query(PathTag).filter_by(tag_id=tag.id, path_id=p.id).first()
        if pt is None:
            pt = PathTag(tag=tag, path=p)
        p.path_tags.append(pt)
        session.add(pt)

    session.add(p)
    return p


def printDots(c):
    if c > 100:
        n = c / 100
        for i in range(n):
            sys.stdout.write('.')
            sys.stdout.flush()
        c = c % 100
    return c


def findMedia(session, root_path, exclude_paths=None):
    num = 0
    c = 0
    for root, dirs, files in os.walk(root_path, topdown=True, followlinks=False):
        dir_path, name = os.path.split(root)
        if name.startswith('.'):
            continue
        if name.startswith('@'):
            continue
        if name.endswith('#'):
            continue
        if name.endswith('~'):
            continue

        # Add 'root' path
        parent_path = addPath(session, root, None)
        c += 1
        num += 1
        session.commit()

        for d in dirs:
            if d.startswith('.'):
                continue
            if d.startswith('@'):
                continue
            if d.endswith('#'):
                continue
            if d.endswith('~'):
                continue

            path = os.path.abspath(os.path.realpath(os.path.join(root, d)))

            if exclude_paths is not None:
                ok = True
                for ex in exclude_paths:
                    if path.startswith(ex):
                        ok = False
                        break
                if ok is False:
                    continue

            addPath(session, path, parent_path)
            session.commit()
            num += 1
            c += 1

        for f in files:
            if f.startswith('.'):
                continue
            if f.startswith('@'):
                continue
            if f.endswith('#'):
                continue
            if f.endswith('~'):
                continue

            path = os.path.abspath(os.path.realpath(os.path.join(root, f)))

            if exclude_paths is not None:
                ok = True
                for ex in exclude_paths:
                    if path.startswith(ex):
                        ok = False
                        break
                if ok is False:
                    continue

            addPath(session, path, parent_path)
            session.commit()
            c += 1
            num += 1

        c = printDots(c)

    return num

