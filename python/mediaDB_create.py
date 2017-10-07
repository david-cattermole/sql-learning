#! /usr/bin/env python
"""
A script to store and categorise a folder of media.
"""

from mediaDB import libbase


def resetMediaTable(db, cursor):
    cursor.execute('DROP TABLE IF EXISTS `MEDIA`;')
    sql = (
        'CREATE TABLE `MEDIA` ('
        '`ID` INT(255) UNSIGNED NOT NULL AUTO_INCREMENT,'
        '`PATH` VARCHAR(500) NOT NULL UNIQUE,'
        '`DIR` VARCHAR(500) NOT NULL,'
        '`NAME` VARCHAR(500) NOT NULL,'
        '`EXT` VARCHAR(255) NOT NULL,'
        '`MIME_TYPE` VARCHAR(255),'
        '`FILE_SIZE` BIGINT,'
        'PRIMARY KEY(`ID`)'
        ') '
        'DEFAULT CHARACTER SET latin1 '
        'COLLATE latin1_general_cs '
        'ENGINE = MyISAM;'
    )
    libbase.commitWrite(db, cursor, sql)
    return


def resetTagsTable(db, cursor):
    cursor.execute('DROP TABLE IF EXISTS `TAGS`;')
    sql = (
        'CREATE TABLE `TAGS` ('
        '`ID`     INT UNSIGNED NOT NULL AUTO_INCREMENT,'
        '`NAME`   VARCHAR(255) NOT NULL,'
        'PRIMARY KEY(`ID`)'
        ')'
        'DEFAULT CHARACTER SET latin1 '
        'COLLATE latin1_general_ci '
        'ENGINE = MyISAM;'
    )
    libbase.commitWrite(db, cursor, sql)
    return


def resetMediaTagsMapTable(db, cursor):
    cursor.execute('DROP TABLE IF EXISTS `MEDIA_TAG_MAP`;')
    sql = (
        'CREATE TABLE `MEDIA_TAG_MAP` ('
        "`MEDIA_ID`    INT UNSIGNED NOT NULL DEFAULT '0',"
        "`TAG_ID`      INT UNSIGNED NOT NULL DEFAULT '0',"
        'PRIMARY KEY(`MEDIA_ID`, `TAG_ID`),'
        'KEY `TAG_FK`(`TAG_ID`),'
        'CONSTRAINT `MEDIA_FK` FOREIGN KEY (`MEDIA_ID`) REFERENCES `MEDIA`(`MEDIA_ID`),'
        'CONSTRAINT `TAG_FK` FOREIGN KEY (`TAG_ID`) REFERENCES `TAGS`(`TAG_ID`)'
        ') '
        'DEFAULT CHARACTER SET latin1 '
        'COLLATE latin1_general_ci '
        'ENGINE MyISAM ;'
    )
    libbase.commitWrite(db, cursor, sql)
    return


def main():
    db = libbase.connectToDatabase()
    cursor = db.cursor()
    libbase.getServerVersion(db, cursor)

    # Reset Table
    print 'Reset Tables...'
    resetMediaTable(db, cursor)
    resetTagsTable(db, cursor)
    resetMediaTagsMapTable(db, cursor)
    
    # disconnect from server
    db.close()


if __name__ == '__main__':
    main()
