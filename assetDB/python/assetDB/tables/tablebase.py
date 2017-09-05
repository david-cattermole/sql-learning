"""
Defines a base table in the Database.
"""

import uuid
import hashlib

from sqlalchemy import (
    MetaData
)
from sqlalchemy.ext.declarative import declarative_base

CODE_LENGTH = 36
NAME_LENGTH = 255
LABEL_LENGTH = 255
DESCRIPTION_LENGTH = 255
COMMENT_LENGTH = 255


def getCode():
    return str(uuid.uuid4())


def getHash(index):
    return str(hashlib.sha1(index).hexdigest())


class BaseTable(object):
    """
    The base table for all tables.
    """
    __auto_name__ = False
    __strictly_typed__ = True
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        # 'mysql_key_block_size': "1024",
    }

    def _setKeywordFields(self, **kwargs):
        # TODO: Add optional 'inclusion / exclusion fields' argument. These
        # would allow explicit inclusion / exclusion of fields being set by
        # this function
        for key in kwargs:
            if key in self.__class__.__dict__:
                setattr(self, key, kwargs[key])
        return

    def __repr__(self):
        result = '<{class_name}('.format(class_name=self.__class__.__name__)
        table = self.__class__.__table__
        columns = table.columns
        for c in columns:
            if c.nullable is True:
                continue
            if c.name in ['code', 'id']:
                continue
            result += '{0}={1!r}, '.format(c.name, getattr(self, c.name))

        # remove trailing ', ' section.
        result = result[:len(result)-2]

        result += ')>'
        return result


#
Base = declarative_base(cls=BaseTable)
metadata = MetaData()


def createTables(engine):
    return Base.metadata.create_all(engine)


def dropTables(engine):
    return Base.metadata.drop_all(engine)
