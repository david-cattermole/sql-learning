"""
Defines a base table in the Database.
"""

import uuid
import datetime
import hashlib
import getpass

from sqlalchemy import (
    MetaData, Column, DateTime, String
)
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID

import assetDB2.setup

CREATED_USER_ID_NAME = 'created_user_id'
CODE_LENGTH = 36
NAME_LENGTH = 255
LABEL_LENGTH = 255
DESCRIPTION_LENGTH = 255
COMMENT_LENGTH = 255


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class ModelBase(object):
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
            else:
                msg = 'key %r could was not found on class %r'
                raise KeyError(msg % (key, self.__class__.__name__))
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
            if c.name.startswith('created_'):
                continue
            if c.name.startswith('updated_'):
                continue
            result += '{0}={1!r}, '.format(c.name, getattr(self, c.name))

        # remove trailing ', ' section.
        result = result[:len(result)-2]

        result += ')>'
        return result


#
Base = declarative_base(cls=ModelBase)
metadata = MetaData()


def createTables(engine):
    return Base.metadata.create_all(engine, checkfirst=True)


def dropTables(engine):
    s = assetDB2.setup.get_session()

    # if assetDB2.setup.DB_TYPE == 'mysql':
    #     # Turn off checks.
    #     s.execute('SET foreign_key_checks = 0;')
    #
    #     # Drop all tables.
    #     for table in Base.metadata.sorted_tables:
    #         # # TODO: Why does this fail, but the below code work?
    #         # txt = text('DROP TABLE IF EXISTS :name CASCADE')
    #         # s.execute(txt, {'name': table.name})
    #
    #         txt = text('DROP TABLE IF EXISTS %s CASCADE' % table.name)
    #         s.execute(txt)
    #
    #     # Turn on checks again.
    #     s.execute('SET foreign_key_checks = 1;')

    # elif assetDB2.setup.DB_TYPE == 'postgres':
    #     for table in Base.metadata.sorted_tables:
    #         txt = text('DROP TABLE IF EXISTS "%s" CASCADE' % table.name)
    #         s.execute(txt)
    #
    #     # # Drop the database schema.
    #     # txt = text('DROP SCHEMA public CASCADE; CREATE SCHEMA public;')
    #     # s.execute(txt)

    # else:
    Base.metadata.drop_all(engine)
    return


