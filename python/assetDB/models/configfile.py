from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from assetDB.models import mixins
from assetDB.models import modelbase as base


class ConfigFileStatus(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'config_file_status'
    __mapper_args__ = {
        'polymorphic_identity': 'ConfigFileStatus',
    }

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
        super(ConfigFileStatus, self).__init__()
        self._setKeywordFields(**kwargs)


class ConfigFileCategory(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'config_file_category'
    __mapper_args__ = {
        'polymorphic_identity': 'ConfigFileCategory',
    }

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
        super(ConfigFileCategory, self).__init__()
        self._setKeywordFields(**kwargs)


class ConfigFile(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'config_file'
    __mapper_args__ = {
        'polymorphic_identity': 'ConfigFile',
    }

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
        super(ConfigFile, self).__init__()
        self._setKeywordFields(**kwargs)


class ConfigFileVersion(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'config_file_version'
    __mapper_args__ = {
        'polymorphic_identity': 'ConfigFileVersion',
    }

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
        super(ConfigFileVersion, self).__init__()
        self._setKeywordFields(**kwargs)
