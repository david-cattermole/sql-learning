from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from assetDB.tables import tablebase as base


class ConfigFileStatus(base.Base):
    __tablename__ = 'config_file_status'
    __mapper_args__ = {
        'polymorphic_identity': 'ConfigFileStatus',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    label = Column(
        'label',
        String(base.LABEL_LENGTH),
        nullable=True,
        unique=False,
    )

    description = Column(
        'description',
        String(base.DESCRIPTION_LENGTH),
        nullable=True,
    )

    config_files = relationship('ConfigFile')

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self._setKeywordFields(**kwargs)


class ConfigFileCategory(base.Base):
    __tablename__ = 'config_file_category'
    __mapper_args__ = {
        'polymorphic_identity': 'ConfigFileCategory',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    label = Column(
        'label',
        String(base.LABEL_LENGTH),
        nullable=True,
        unique=False,
    )

    description = Column(
        'description',
        String(base.DESCRIPTION_LENGTH),
        nullable=True,
    )

    config_files = relationship('ConfigFile')

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self._setKeywordFields(**kwargs)


class ConfigFile(base.Base):
    __tablename__ = 'config_file'
    __mapper_args__ = {
        'polymorphic_identity': 'ConfigFile',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    code = Column(
        'code',
        String(base.CODE_LENGTH),
        nullable=False,
        unique=True,
    )

    config_file_status_id = Column(
        'config_file_status_id',
        Integer,
        ForeignKey(
            'config_file_status.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    config_file_status = relationship(
        'ConfigFileStatus',
        foreign_keys=[config_file_status_id]
    )

    config_file_category_id = Column(
        'config_file_category_id',
        Integer,
        ForeignKey(
            'config_file_category.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    config_file_category = relationship(
        'ConfigFileCategory',
        foreign_keys=[config_file_category_id]
    )

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=False,
    )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class ConfigFileVersion(base.Base):
    __tablename__ = 'config_file_version'
    __mapper_args__ = {
        'polymorphic_identity': 'ConfigFileVersion',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    config_file_id = Column(
        'config_file_id',
        Integer,
        ForeignKey(
            'config_file.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    config_file = relationship(
        'ConfigFile',
        foreign_keys=[config_file_id]
    )

    version = Column(
        'version',
        Integer,
        nullable=False,
        unique=False,
    )

    revision = Column(
        'revision',
        Integer,
        nullable=False,
        unique=False,
    )

    approved = Column(
        'approved',
        Boolean,
        nullable=True,
        unique=False,
    )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)
