#! /usr/bin/env python
"""
A script to store and categorise a folder of media.
"""

import sys

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

    # TODO: Copy the same functionallity as
    # 'mediaDB/python/filePathsFromTag.py', but with SQLAlchemy instead.
    raise NotImplementedError


if __name__ == '__main__':
    main()
