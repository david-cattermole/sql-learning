#! /usr/bin/env python
"""
A script to store and categorise a folder of media.
"""

import sys

from mediaDB import libget
from mediaDB import libbase


def main():
    # print 'args', sys.argv
    maxNum = 10
    print sys.argv
    if len(sys.argv) == 2:
        maxNum = int(sys.argv[1])
    
    db = libbase.connectToDatabase()
    cursor = db.cursor()
    libbase.getServerVersion(db, cursor)

    # Get tags.
    tagIds = libget.getTagIdsByCount(db, cursor, maxNum=maxNum)
    for i, tagId in enumerate(tagIds):
        tagName = libget.getTagNameFromTagId(db, cursor, tagId[1])
        print ('> count=' + str(tagId[0])), ('name=' + repr(tagName))

    # disconnect from server
    db.close()

if __name__ == '__main__':
    main()
