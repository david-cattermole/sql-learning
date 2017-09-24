#! /usr/bin/env python
"""
A script to store and categorise a folder of media.
"""

import sys

from sqlalchemy import func, desc

import mediaDB.setup as setup
from mediaDB.models import *


def main():
    # print 'args', sys.argv
    maxNum = 10
    if len(sys.argv) == 2:
        maxNum = int(sys.argv[1])

    session = setup.get_session()

    # Get tags.
    q = session.query(func.count(PathTag.tag_id), PathTag)
    q = q.group_by(PathTag.tag_id).order_by(desc(func.count(PathTag.tag_id)))
    q = q.limit(maxNum)
    records = q.all()
    print 'records', records
    for record in records:
        count, path_tag = record
        print ('> count=' + str(count)), ('name=' + repr(path_tag.tag.name))

if __name__ == '__main__':
    main()
