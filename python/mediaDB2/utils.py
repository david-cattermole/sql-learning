"""
File Data database tables
"""

import mimetypes
import os
import os.path
import re
import sys
import time

import enchant

# from sqlalchemy import *

import mediaDB2.config as config
import mediaDB2.mounts
from mediaDB2.cache import memoized
from mediaDB2.models import (
    Path, Repository, MimeType, MimeSubtype, Mime, Tag, PathTag
)

# initialise mimetypes with user-defined values.
mime_files = config.getMimeFilePaths()
mimetypes.init(mime_files)

SPLIT_CHARS = config.getSplitChars()
UNNEEDED_WORDS = config.getExcludedWords()

SPELLER = enchant.Dict()


@memoized
def spelling_check(name):
    return SPELLER.check(name)


@memoized
def createTagNames(path):
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

        # File Extension
        n, ext = os.path.splitext(path)
        file_ext = ext[1:].lower()
        if tag == file_ext:
            continue

        # Check Spelling
        if not spelling_check(tag):
            continue

        # Add
        if tag not in the_tags:
            the_tags.append(tag)
    return the_tags


def findRepo(session, hostname, share):
    q = session.query(Repository)
    q = q.filter(Repository.host_name == hostname, Repository.share_name == share)
    repo = q.first()
    return repo


def createRepo(session, mount):
    hostname = mount['hostname']
    share = mount['share']
    if isinstance(hostname, basestring) and len(hostname) == 0:
        return None
    if isinstance(share, basestring) and len(share) == 0:
        return None

    repo = findRepo(session, hostname, share)
    if repo is None:
        repo = Repository(host_name=hostname, share_name=share)
    return repo


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
    mount_dir, mount = mediaDB2.mounts.getMount(mediaDB2.mounts.MOUNTS, full_path)
    if mount:
        repository = createRepo(session, mount)
    if repository is None:
        msg = 'Warning: Could not create repository for file path, %r.'
        print msg % full_path
        return None
    session.add(repository)

    # Get the final end_path
    end_path = full_path[len(mount_dir):]
    end_path = end_path.encode('ascii', errors='ignore')
    end_path_len = len(end_path.strip())
    if end_path_len == 0:
        return None
    elif end_path_len > 255:
        msg = 'Warning: File path exceeds allowed character length, %r.'
        print msg % full_path
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

    else:
        msg = 'Warning: File path is invalid, %r.'
        print msg % full_path
        return None

    # Parent directory
    if parent_path is not None:
        p.parent = parent_path

    # Repository
    p.repository = repository

    # Tags
    # NOTE: Only use file name for tags.
    dir_path, file_name = os.path.split(full_path)
    tag_names = createTagNames(file_name)
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
    total_add_time = 0.0

    num = 0
    c = 0
    for root, dirs, files in os.walk(root_path, topdown=True, followlinks=False):
        paths = []
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
        s = time.time()
        parent_path = addPath(session, root, None)
        c += 1
        num += 1
        session.commit()
        e = time.time()
        total_add_time += e - s

        # Get all the directories paths
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

            num += 1
            paths.append(path)

        # Get all the file paths
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

            num += 1
            paths.append(path)

        # Add paths to database
        s = time.time()
        for path in paths:
            parent = parent_path
            if parent_path is not None:
                if not path.startswith(parent_path.full_path):
                    parent = None
            addPath(session, path, parent)
            session.commit()
            c += 1
        e = time.time()
        total_add_time += e - s

        c = printDots(c)

    print ''
    print '+' * 20
    print 'Total Add Time:', total_add_time
    print '+' * 20
    return num
