#! /usr/bin/env python
"""
A script to store and categorise a folder of media.
"""

import mimetypes
import os
import os.path
import re
import sys
import time

from mediaDB import libbase

# initialise mimetypes with user-defined values.
files = libbase.getMimeFilePaths()
mimetypes.init(files)

SPLIT_CHARS = libbase.getSplitChars()
UNNEEDED_WORDS = libbase.getExcludedWords()


class File(object):
    def __init__(self, path, root_path):
        super(File, self).__init__()
        path = path.encode('ascii', errors='ignore')
        self.path = path

        dirname, name = os.path.split(path)
        self.dirname = dirname.encode()
        self.name = name.encode()

        split = path.split(os.sep)
        self.folderType = split[1]

        # File Extension
        n, ext = os.path.splitext(path)
        self.extension = ext[1:].lower()

        # MIME Type
        mime_type = mimetypes.guess_type(self.path, strict=False)
        if mime_type and len(mime_type) == 2 and mime_type[0]:
            self.mime_type = mime_type[0]
        else:
            self.mime_type = 'unknown'

        # Tags
        tagPath = self.path[len(root_path)-1:]
        self.tags = self.__createTags(tagPath, self.extension)

        # Size
        try:
            self.size = os.path.getsize(path)
        except:
            self.size = 0

        return

    def __createTags(self, path, file_ext):
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


def addMedia(f, db, cursor):
    sql = (
        'INSERT INTO `MEDIA`(`PATH`, `NAME`, `DIR`, `EXT`, `MIME_TYPE`, `FILE_SIZE`) '
        'VALUES (%s, %s, %s, %s, %s, %s) '
        'ON DUPLICATE KEY UPDATE `PATH`=%s, `NAME`=%s, `DIR`=%s, `EXT`=%s, `MIME_TYPE`=%s, `FILE_SIZE`=%s;'
    )
    libbase.commitWrite(db, cursor, sql, (f.path, f.name, f.dirname, f.extension, f.mime_type, f.size,
                                          f.path, f.name, f.dirname, f.extension, f.mime_type, f.size))

    # Get Media ID
    sql = 'SELECT `ID` FROM `MEDIA` WHERE `PATH`=%s ;'
    mediaIds = libbase.commitReadAll(db, cursor, sql, (f.path,))
    if len(mediaIds) > 1:
        print 'mediaIds:', mediaIds
        print 'path:', f.path
        print 'tags:', f.tags
        assert False
    mediaId = mediaIds[0]

    # Add Tags
    tagIds = []
    if f.tags:
        for tag in f.tags:
            # Get Tag ID
            sql = 'SELECT `ID` FROM `TAGS` WHERE `NAME`=%s;'
            tagIds = libbase.commitReadAll(db, cursor, sql, (tag,))
            tagId = None
            if len(tagIds) > 0:
                tagId = tagIds[0]

            # Add Tag
            if not tagId:
                sql = 'INSERT INTO `TAGS`(`NAME`) VALUES(%s);'
                libbase.commitWrite(db, cursor, sql, (tag,))

                # Get Tag ID, now that it's definitely in there.
                sql = 'SELECT `ID` FROM `TAGS` WHERE `NAME`=%s;'
                tagId = libbase.commitReadOne(db, cursor, sql, (tag,))

            # Add mapping between media and tag.
            sql = (
                'INSERT INTO `MEDIA_TAG_MAP`(`MEDIA_ID`, `TAG_ID`) '
                'VALUES(%s, %s)'
                'ON DUPLICATE KEY UPDATE `MEDIA_ID`=%s, `TAG_ID`=%s;'
            )
            libbase.commitWrite(db, cursor, sql, (mediaId[0], tagId[0], mediaId[0], tagId[0],))
    return


def findMedia(db, cursor, root_path, exclude=None):
    c = 0
    num = 0
    for root, dirs, files in os.walk(root_path, topdown=True, followlinks=False):
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
                try:
                    files = os.listdir(dirpath)
                except:
                    pass
            for filename in sorted(files):
                if filename.startswith('.'):
                    continue
                if filename.startswith('@'):
                    continue
                if filename.endswith('#'):
                    continue
                if filename.endswith('~'):
                    continue

                path = os.path.abspath(os.path.join(dirpath, filename))
                if not os.path.isfile(path):
                    continue

                if exclude is not None:
                    ok = True
                    for ex in exclude:
                        if path.startswith(ex):
                            ok = False
                            break
                    if ok is False:
                        continue

                f = File(path, root_path)
                addMedia(f, db, cursor)

                c += 1
                num += 1
                if c > 100:
                    c = 0
                    sys.stdout.write('.')
                    sys.stdout.flush()
                del f
    return num


def main():
    db = libbase.connectToDatabase()
    cursor = db.cursor()
    libbase.getServerVersion(db, cursor)

    # Find Media
    include = libbase.getIncludePaths()
    exclude = libbase.getExcludePaths()
    for path in include:
        print 'Find Media...', path
        s = time.time()
        num = findMedia(db, cursor, path, exclude=exclude)
        e = time.time()
        total = e - s
        print ''
        print 'Path =', path
        print 'Count =', str(num)
        print 'Per-Insert Time = %.4g seconds' % (total / num)
        print 'Total Time = %.4g seconds' % total
        print 'Finished.'

    # disconnect from server
    db.close()


if __name__ == '__main__':
    main()
