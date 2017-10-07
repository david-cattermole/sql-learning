#! /usr/bin/env python
"""
A script to store and categorise a folder of media.
"""

import libbase


def getTagIdFromTagName(db, cursor, tagName):
    sql = (
        'SELECT `ID` FROM `TAGS` WHERE `NAME`={name!r};'
    )
    sql = sql.format(name=tagName)
    tagId = libbase.commitReadOne(db, cursor, sql)
    if tagId and len(tagId) > 0:
        tagId = tagId[0]
    else:
        tagId = -1
    return tagId


def getTagNameFromTagId(db, cursor, tagId):
    sql = (
        'SELECT `NAME` FROM `TAGS` WHERE `ID`={id};'
    )
    sql = sql.format(id=tagId)
    tagName = libbase.commitReadOne(db, cursor, sql)
    if tagName and len(tagName) > 0:
        tagName = tagName[0]
    else:
        tagName = ''
    return tagName


def getFieldFromTable(db, cursor, table,
                      field=None,
                      dbfilter=None,
                      dbsort=None):
    assert isinstance(table, str)
    if field is None:
        field = '*'
    if dbfilter is None:
        dbfilter = '1'
    if dbsort is None:
        dbsort = '1'
    sql = (
        'SELECT {field} '
        'FROM {table} '
        'WHERE {dbfilter} '
        'ORDER BY {dbsort} ;'
    )
    sql = sql.format(field=field, table=table, dbfilter=dbfilter, dbsort=dbsort)
    values = libbase.commitReadAll(db, cursor, sql)
    return values


def getAllTagNames(db, cursor):
    table = '`TAGS`'
    field = '`NAME`'
    return getFieldFromTable(db, cursor, table, field)


def getAllTags(db, cursor):
    table = '`TAGS`'
    field = None
    return getFieldFromTable(db, cursor, table, field=field)


def getAllMedia(db, cursor):
    table = '`MEDIA`'
    field = None
    return getFieldFromTable(db, cursor, table, field=field)


def getAllMediaObjects(db, cursor, mediaType=None):
    table = '`MEDIA`'
    field = None
    dbfilter = None
    if mediaType is not None:
        dbfilter = '`MIME_TYPE` LIKE {0!r}'.format(mediaType)
    dbsort = '`NAME`, `FILE_SIZE`'

    media = []
    mediaValues = getFieldFromTable(db, cursor, table, field=field,
                                    dbfilter=dbfilter,
                                    dbsort=dbsort)
    for mediaValue in mediaValues:
        if mediaValue:
            mediaId = mediaValue[0]
            tags = getTagsFromMediaId(db, cursor, mediaId)
            m = libbase.Media(mediaValue)
            media.append(m)
    return media


def getAllMediaNames(db, cursor):
    table = '`MEDIA`'
    field = '`NAME`'
    return getFieldFromTable(db, cursor, table, field=field)


def getTagsFromMediaId(db, cursor, mediaId):
    tags = []

    # Get Media Ids
    sql = (
        'SELECT `TAG_ID` '
        'FROM `MEDIA_TAG_MAP` '
        'WHERE `MEDIA_ID`={mediaid};')
    sql = sql.format(mediaid=mediaId)
    tagIds = libbase.commitReadAll(db, cursor, sql)

    for tagId in tagIds:
        tagName = getTagNameFromTagId(db, cursor, tagId[0])
        if tagName:
            tags.append(tagName)

    return tags


def searchMediaTags(db, cursor, tagNames, mediaType):
    tagIds = []
    for tagName in tagNames:
        tagId = getTagIdFromTagName(db, cursor, tagName)
        if tagId and tagId not in tagIds and tagId != -1:
            tagIds.append(int(tagId))
    if len(tagIds) == 0:
        return []

    dbfilter = ''
    for i, tagId in enumerate(tagIds):
        dbfilter += '`TAG_ID`={0}'.format(tagId)
        if i < len(tagIds)-1:
            dbfilter += ' OR '

    sql = (
        'SELECT COUNT(`TAG_ID`), `MEDIA_ID` '
        'FROM `MEDIA_TAG_MAP` '
        'WHERE ' + dbfilter + ' '
        'GROUP BY `MEDIA_ID` '
        'HAVING COUNT(`TAG_ID`) > {length}'
    )
    sql = sql.format(length=len(tagIds)-1)
    values = libbase.commitReadAll(db, cursor, sql)
    mediaIds = []
    for value in values:
        if value and len(value) > 1:
            mediaIds.append(value[1])

    media = []
    sqlFormat = (
        'SELECT * '
        'FROM `MEDIA`'
        'WHERE `ID`={mid} AND `MIME_TYPE` LIKE {mtype!r} '
        'ORDER BY `PATH`;'
    )
    for mediaId in mediaIds:
        sql = sqlFormat.format(mid=mediaId, mtype=mediaType)
        m = libbase.commitReadAll(db, cursor, sql)
        if len(m) > 0:
            tags = getTagsFromMediaId(db, cursor, mediaId)
            media.append(libbase.Media(m[0], tags=tags))
    return media


def getTagIdsByCount(db, cursor, maxNum=None):
    sql = (
        'SELECT COUNT(`TAG_ID`), `TAG_ID` '
        'FROM `MEDIA_TAG_MAP` '
        'GROUP BY `TAG_ID` '
        'ORDER BY COUNT(`TAG_ID`) DESC;'
    )
    values = libbase.commitReadAll(db, cursor, sql)
    tagIds = []
    count = 0
    for value in values:
        if value and len(value) > 1:
            tagIds.append(value)
            count += 1
        if count >= maxNum:
            break
    return tagIds
