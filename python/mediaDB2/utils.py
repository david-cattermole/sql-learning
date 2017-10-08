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
    for d in mounts.keys():
        if path.startswith(d) is True:
            mount = mounts[d]
            break
    return mount


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


def loopFiles(session, files, dirpath, exclude, parent_dir):
    paths = []
    for filename in files:
        if filename.startswith('.'):
            continue
        if filename.startswith('@'):
            continue
        if filename.endswith('#'):
            continue
        if filename.endswith('~'):
            continue

        full_path = os.path.abspath(os.path.join(dirpath, filename))
        if not os.path.isfile(full_path):
            continue

        if exclude is not None:
            ok = True
            for ex in exclude:
                if full_path.startswith(ex):
                    ok = False
                    break
            if ok is False:
                continue

        # Size
        try:
            size = os.path.getsize(full_path)
        except:
            size = 0

        # MIME type
        mime = createMime(session, full_path)
        session.commit()

        # Repository
        mount = getMount(MOUNTS, full_path)
        repository = None
        if mount:
            repository = createRepo(session, mount)
        session.commit()

        # Path
        p = Path(path=full_path, is_file=True, file_size=size)
        p.mime = mime
        p.repository = repository
        p.parent = parent_dir
        paths.append(p)

        # File Extension
        n, ext = os.path.splitext(full_path)
        extension = ext[1:].lower()

        # Tags
        path = full_path[len(dirpath):]  # Only use file name for tags.
        tag_names = createTags(path, extension)
        for name in tag_names:
            tag = session.query(Tag).filter_by(name=name).first()
            if tag is None:
                tag = Tag(name=name)
                session.add(tag)
            pt = PathTag(tag=tag, path=p)
            p.path_tags.append(pt)

        session.commit()

    return paths


def printDots(c):
    if c > 100:
        n = c / 100
        for i in range(n):
            sys.stdout.write('.')
            sys.stdout.flush()
        c = c % 100
    return c


def findMedia(session, root_path, excludes=None):
    c = 0
    num = 0
    root_dir_objs = {}
    for root, dirs, files in os.walk(root_path, topdown=True, followlinks=False):
        # TODO: On Windows, get proper 'repo' path. Something like
        # "\\HEARTOFGOLD\Music".

        # Repository
        mount = getMount(MOUNTS, root)
        repository = None
        if mount:
            repository = createRepo(session, mount)
        session.add_all([repository])

        d = None
        if root not in root_dir_objs:
            d = Path(path=root, is_file=False)
            root_dir_objs[root] = d
            session.add(d)
            num += 1
            c += 1
        else:
            d = root_dir_objs[root]

        paths = loopFiles(session, files, root, excludes, d)
        num_paths = len(paths)
        num += num_paths
        c += num_paths

        session.add_all(paths)
        session.commit()

        c = printDots(c)

        for dirname in dirs:
            if dirname.startswith('.'):
                continue
            if dirname.startswith('@'):
                continue
            if dirname.endswith('#'):
                continue
            if dirname.endswith('~'):
                continue

            files = []
            dirpath = os.path.abspath(os.path.join(root, dirname))
            if os.path.isdir(dirpath):
                d = Path(path=dirpath, is_file=False)
                session.add(d)
                num += 1
                c += 1

                try:
                    files = os.listdir(dirpath)
                except:
                    continue

                paths = loopFiles(session, files, dirpath, excludes, d)
                num_paths = len(paths)
                num += num_paths
                c += num_paths
                session.add_all(paths)
                session.commit()

                c = printDots(c)

    return num

