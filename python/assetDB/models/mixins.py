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

from assetDB.models import modelbase as base


def get_site_name():
    value = os.getenv('SITE', 'unknown')
    return value.lower()


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


class LabelMixin(object):
    label = Column(
        'label',
        String(base.LABEL_LENGTH),
        nullable=True,
        unique=True,
    )


class DescriptionMixin(object):
    description = Column(
        'description',
        String(base.DESCRIPTION_LENGTH),
        nullable=True,
    )


class CreatedUpdatedMixin(object):
    # define 'create_date' to default to now()
    created_datetime = Column(
        'created_datetime',
        DateTime(timezone=True),
        default=func.now()
    )

    created_user_name = Column(
        'created_user_name',
        String(base.NAME_LENGTH),
        nullable=False,
        default=getpass.getuser
    )

    @declared_attr
    def created_user(cls):
        clsname = cls.__name__
        prijoin = '{cn}.created_user_name==User.user_name'.format(cn=clsname)
        foreign_keys = '{cn}.created_user_name'.format(cn=clsname)
        return relationship(
            'User',
            primaryjoin=prijoin,
            foreign_keys=foreign_keys,
        )

    created_site_name = Column(
        'created_site_name',
        String(base.NAME_LENGTH),
        nullable=False,
        default=get_site_name
    )

    @declared_attr
    def created_site(cls):
        clsname = cls.__name__
        prijoin = '{cn}.created_site_name==Site.name'.format(
            cn=clsname)
        foreign_keys = '{cn}.created_site_name'.format(cn=clsname)
        return relationship(
            'Site',
            primaryjoin=prijoin,
            foreign_keys=foreign_keys,
        )

    # TODO: Should we define 'updated_datetime' to use the current_timestamp SQL function on update
    updated_datetime = Column(
        'updated_datetime',
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now()
        # onupdate=func.current_timestamp()  # TODO: Should we use now or current_timestamp?
    )

    updated_user_name = Column(
        'updated_user_name',
        String(base.NAME_LENGTH),
        nullable=False,
        default=getpass.getuser,
        onupdate=getpass.getuser,
    )

    @declared_attr
    def updated_user(cls):
        clsname = cls.__name__
        prijoin = '{cn}.updated_user_name==User.user_name'.format(cn=clsname)
        foreign_keys = '{cn}.updated_user_name'.format(cn=clsname)
        return relationship(
            'User',
            primaryjoin=prijoin,
            foreign_keys=foreign_keys,
        )

    updated_site_name = Column(
        'updated_site_name',
        String(base.NAME_LENGTH),
        nullable=False,
        default=get_site_name,
        onupdate=get_site_name
    )

    @declared_attr
    def updated_site(cls):
        clsname = cls.__name__
        prijoin = '{cn}.updated_site_name==Site.name'.format(cn=clsname)
        foreign_keys = '{cn}.updated_site_name'.format(cn=clsname)
        return relationship(
            'Site',
            primaryjoin=prijoin,
            foreign_keys=foreign_keys,
        )
