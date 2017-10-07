#! /usr/bin/env python
"""
A script to store and categorise a folder of media.
"""

import sys

import mediaDB2.setup as setup


def main():
    # print 'args', sys.argv
    maxNum = 25
    if len(sys.argv) == 2:
        maxNum = int(sys.argv[1])

    session = setup.get_session()

    # Get tags.
    # t = session.query(func.count(PathTag.tag_id), PathTag)
    # t = t.group_by(PathTag.tag_id, PathTag.path_id)
    # t = t.order_by(func.count(PathTag.tag_id))
    # t = t.subquery('t')
    #
    # q = session.query(func.count(PathTag.tag_id), PathTag)
    # q = q.join(t)
    # q = q.limit(maxNum)

#     s = """
# SELECT path_tag.tag_id, path_tag.path_id, t.cnt
# FROM (
#     SELECT path_tag.tag_id, COUNT(path_tag.tag_id) AS cnt
#     FROM path_tag
#     GROUP BY path_tag.tag_id
#     ) t JOIN path_tag m ON m.tag_id = t.tag_id AND t.cnt = m.cnt;
# """
#     q = session.execute(s)

    # q = session.query(func.count(PathTag.tag_id), PathTag)
    # q = q.group_by(PathTag.tag_id, PathTag.path_id)
    # q = q.order_by(func.count(PathTag.tag_id))
    # q = q.limit(maxNum)
    records = q.all()
    # print 'records', records
    for record in records:
        count, path_tag = record
        print ('> count=' + str(count)), ('name=' + repr(path_tag.tag.name))

if __name__ == '__main__':
    main()
