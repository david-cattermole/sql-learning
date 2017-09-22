"""
Asset Data database tables
"""
from sqlalchemy import (
    Column, Integer, String, Numeric, Boolean, ForeignKey, DateTime,
)
from sqlalchemy.orm import relationship, backref
from assetDB.models import mixins
from assetDB.models import modelbase as base


class Project(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'project'
    __mapper_args__ = {
        'polymorphic_identity': 'Project',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(Project, self).__init__()
        self._setKeywordFields(**kwargs)


class Sequence(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'sequence'
    __mapper_args__ = {
        'polymorphic_identity': 'Sequence'
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=False,
    )

    def __init__(self, **kwargs):
        super(Sequence, self).__init__()
        self._setKeywordFields(**kwargs)


class Shot(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'shot'
    __mapper_args__ = {
        'polymorphic_identity': 'Shot'
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=False,
    )

    def __init__(self, **kwargs):
        super(Shot, self).__init__()
        self._setKeywordFields(**kwargs)


class Name(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'name'
    __mapper_args__ = {
        'polymorphic_identity': 'Name',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    asset_datas = relationship('Asset')

    def __init__(self, **kwargs):
        super(Name, self).__init__()
        self._setKeywordFields(**kwargs)


class Subname(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'subname'
    __mapper_args__ = {
        'polymorphic_identity': 'Subname',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    asset_datas = relationship('Asset')

    def __init__(self, **kwargs):
        super(Subname, self).__init__()
        self._setKeywordFields(**kwargs)


class Variant(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'variant'
    __mapper_args__ = {
        'polymorphic_identity': 'Variant',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    asset_datas = relationship('Asset')

    def __init__(self, **kwargs):
        super(Variant, self).__init__()
        self._setKeywordFields(**kwargs)


class Resolution(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'resolution'
    __mapper_args__ = {
        'polymorphic_identity': 'Resolution',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    asset_datas = relationship('Asset')

    def __init__(self, **kwargs):
        super(Resolution, self).__init__()
        self._setKeywordFields(**kwargs)


class Instance(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'instance'
    __mapper_args__ = {
        'polymorphic_identity': 'Instance',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    asset_datas = relationship('Asset')

    def __init__(self, **kwargs):
        super(Instance, self).__init__()
        self._setKeywordFields(**kwargs)


class Type(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'type'
    __mapper_args__ = {
        'polymorphic_identity': 'Type',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    asset_datas = relationship('Asset')

    def __init__(self, **kwargs):
        super(Type, self).__init__()
        self._setKeywordFields(**kwargs)


class MediaVersion(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'media_version'
    __mapper_args__ = {
        'polymorphic_identity': 'MediaVersion',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(MediaVersion, self).__init__()
        self._setKeywordFields(**kwargs)


class Task(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'task'
    __mapper_args__ = {
        'polymorphic_identity': 'Task',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(Task, self).__init__()
        self._setKeywordFields(**kwargs)

