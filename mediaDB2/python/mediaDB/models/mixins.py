import os
import uuid
import datetime
import hashlib
import getpass

from sqlalchemy import (
    Column, Integer, String, ForeignKey, MetaData, DateTime
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from mediaDB.models import modelbase as base


class IdentityMixin(object):
    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    code = Column(
        'code',
        base.GUID,
        default=uuid.uuid4,
        nullable=False,
        unique=True
    )

