#! /usr/bin/env python
"""
A script to store and categorise a folder of media.
"""

import sys

from mediaDB import libget
from mediaDB import libbase


def main():
    # print 'args', sys.argv
    media_type = None
    search_tags = []
    if len(sys.argv) < 2:
        print 'fail'
        return
    if len(sys.argv) > 1:
        if sys.argv[1] == '<all>':
            media_type = None
        else:
            media_type = str(sys.argv[1])
        search_tags = sys.argv[2:]

    db = libbase.connectToDatabase()
    cursor = db.cursor()
    libbase.getServerVersion(db, cursor)

    print 'Searching for:', repr(','.join(search_tags)), 'as type:', repr(media_type)

    # if media_type == 'image':
    #     print 'Images' + ('-' * 100)
    #     media = libget.searchMediaTags(db, cursor, search_tags, 'image/%')
    #     print 'found', len(media)
    #     for m in media:
    #         print '> ', m.path
    #
    # elif media_type == 'music':
    #     print 'Music' + ('-' * 100)
    #     media = libget.searchMediaTags(db, cursor, search_tags, 'audio/%')
    #     print 'found', len(media)
    #     for m in media:
    #         print '> ', m.path
    #
    # elif media_type == 'video':
    #     print 'Videos' + ('-' * 100)
    #     media = libget.searchMediaTags(db, cursor, search_tags, 'video/%')
    #     print 'found', len(media)
    #     for m in media:
    #         print '> ', m.path
    # else:
    print 'Files' + ('-' * 100)
    media_type_search = media_type
    if media_type is not None:
        media_type_search = '%' + media_type + '%'
    media = libget.searchMediaTags(db, cursor, search_tags, media_type_search)
    print 'found', len(media)
    for m in media:
        print '> ', m.path

    db.close()

if __name__ == '__main__':
    main()
