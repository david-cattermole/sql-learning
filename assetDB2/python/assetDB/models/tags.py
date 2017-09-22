"""
Asset Data database tables
"""
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, ForeignKey, DateTime,
)
from sqlalchemy.orm import relationship, backref
from assetDB.models import mixins
from assetDB.models import modelbase as base


class Tag(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'tag'
    __mapper_args__ = {
        'polymorphic_identity': 'Tag',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(Tag, self).__init__()
        self._setKeywordFields(**kwargs)


class Key(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'key'
    __mapper_args__ = {
        'polymorphic_identity': 'Key',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(Key, self).__init__()
        self._setKeywordFields(**kwargs)


class Value(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'value'
    __mapper_args__ = {
        'polymorphic_identity': 'Value',
    }

    value_integer = Column(
        'value_integer',
        Integer,
        nullable=True,
        unique=False,
    )

    value_float = Column(
        'value_float',
        Float(53),
        nullable=True,
        unique=False,
    )

    value_string = Column(
        'value_string',
        String(base.COMMENT_LENGTH),
        nullable=True,
        unique=False,
    )

    def get_value(self):
        value = None
        if self.value_float is not None:
            value = self.value_float
        elif self.value_integer is not None:
            value = self.value_integer
        elif self.value_string is not None:
            value = self.value_string
        return value

    def set_value(self, value):
        self.value_float = None
        self.value_integer = None
        self.value_string = None
        if isinstance(value, float):
            self.value_float = value
        elif isinstance(value, int):
            self.value_integer = value
        elif isinstance(value, basestring):
            self.value_string = str(value)
        else:
            raise ValueError
        return

    value = property(get_value, set_value)

    def __init__(self, value):
        super(Value, self).__init__()
        self.value = value
