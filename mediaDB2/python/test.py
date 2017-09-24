"""
Test script for assetDB.
"""
import mimetypes
import os
import os.path

import sys
import time

from sqlalchemy import create_engine

import mediaDB.setup as setup
import mediaDB.config as config
import mediaDB.models.modelbase as base
import mediaDB.models.path
from mediaDB.models import *

# initialise mimetypes with user-defined values.
mime_files = config.getMimeFilePaths()
mimetypes.init(mime_files)

SPLIT_CHARS = config.getSplitChars()
UNNEEDED_WORDS = config.getExcludedWords()


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
        mime_type, mime_subtype = mediaDB.models.path.createMime(session, full_path)

        # Path

        p = Path(path=full_path, is_file=True, file_size=size,
                 mime_type=mime_type,
                 mime_subtype=mime_subtype)
        p.parent = parent_dir
        paths.append(p)

        # File Extension
        n, ext = os.path.splitext(full_path)
        extension = ext[1:].lower()

        # Tags
        path = full_path[len(dirpath):]  # Only use file name for tags.
        tag_names = mediaDB.models.path.createTags(path, extension)
        for name in tag_names:
            tag = session.query(Tag).filter_by(name=name).first()
            if tag is None:
                tag = Tag(name=name)
                session.add(tag)
            pt = PathTag(tag=tag, path=p)
            p.path_tags.append(pt)

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
    # all_paths = []

    # d = Path(path=root_path, is_file=False)
    # session.add(d)

    c = 0
    num = 0
    root_dir_objs = {}
    for root, dirs, files in os.walk(root_path, topdown=True, followlinks=False):
        # TODO: Get proper 'repo' path. Something like "\\HEARTOFGOLD\Music".
        repo_path = root

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


def main():
    url = setup.get_database_url()
    engine = create_engine(url, echo=setup.ECHO)

    # Reset Tables
    base.dropTables(engine)
    base.createTables(engine)

    session = setup.get_session()

    # Find Media
    includes = config.getIncludePaths()
    excludes = config.getExcludePaths()
    for path in includes:
        print 'Find Media...', path
        s = time.time()

        num = findMedia(session, path, excludes=excludes)

        e = time.time()
        total = e - s
        per_total = 0.0
        if num > 0:
            per_total = (total / num)

        print ''
        print 'Path =', path
        print 'Count =', str(num)
        print 'Per-Insert Time = %.4g seconds' % per_total
        print 'Total Time = %.4g seconds' % total
        print 'Finished.'


if __name__ == '__main__':
    main()
