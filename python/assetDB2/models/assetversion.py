"""
Asset Data database tables
"""
import os

from sqlalchemy import (
    Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import relationship

from assetDB2.models import mixins
from assetDB2.models import modelbase as base


class AssetVersion(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_version'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetVersion',
    }
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }

    asset_id = Column(
        'asset_id', Integer,
        ForeignKey('asset.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )

    media_version_id = Column(
        'media_version_id', Integer,
        ForeignKey('media_version.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True
    )

    task_id = Column(
        'task_id', Integer,
        ForeignKey('task.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True
    )

    comment = Column(
        'comment',
        String(base.COMMENT_LENGTH),
        nullable=True,
        unique=False,
    )

    version = Column(
        'version',
        Integer,
        nullable=False,
        unique=False,
    )

    asset = relationship('Asset')

    media_version = relationship('MediaVersion')

    task = relationship('Task')

    tags = relationship(
        'Tag',
        secondary='asset_version_tag',
    )

    status_tags = relationship(
        'Tag',
        secondary='asset_version_status_tag',
    )

    key_values = relationship(
        'AssetVersionKeyValue',
        secondary='asset_version_key_value',
        secondaryjoin='AssetVersionKeyValue.asset_version_id==AssetVersion.id',
    )

    incoming_assets = relationship(
        'AssetVersionDependency',
        secondary='asset_version_dependency',
        primaryjoin='AssetVersionDependency.destination_id==AssetVersion.id',
        secondaryjoin='AssetVersionDependency.destination_id==AssetVersion.id'
    )

    outgoing_assets = relationship(
        'AssetVersionDependency',
        secondary='asset_version_dependency',
        primaryjoin='AssetVersionDependency.source_id==AssetVersion.id',
        secondaryjoin='AssetVersionDependency.source_id==AssetVersion.id'
    )

    def __init__(self, **kwargs):
        super(AssetVersion, self).__init__()
        self._setKeywordFields(**kwargs)

    def get_path(self):
        path = self.asset.path
        version = 'v' + str(self.version).zfill(3)
        path = os.path.join(path, version)
        return path

    path = property(get_path)


class AssetVersionTag(base.Base, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_version_tag'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetVersionTag',
    }

    tag_id = Column(
        'tag_id',
        Integer,
        ForeignKey('tag.id'),
        primary_key=True,
        autoincrement=True,
    )

    asset_version_id = Column(
        'asset_version_id',
        Integer,
        ForeignKey('asset_version.id'),
        primary_key=True,
    )

    tag = relationship('Tag')

    asset_version = relationship('AssetVersion')

    def __init__(self, tag, asset_version):
        super(AssetVersionTag, self).__init__()
        self.tag = tag
        self.asset_version = asset_version


class AssetVersionStatusTag(base.Base, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_version_status_tag'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetVersionStatusTag',
    }

    tag_id = Column(
        'tag_id',
        Integer,
        ForeignKey('tag.id'),
        primary_key=True,
        autoincrement=True,
    )

    asset_version_id = Column(
        'asset_version_id',
        Integer,
        ForeignKey('asset_version.id'),
        primary_key=True,
    )

    tag = relationship('Tag')

    asset_version = relationship('AssetVersion')

    def __init__(self, tag, asset_version):
        super(AssetVersionStatusTag, self).__init__()
        self.tag = tag
        self.asset_version = asset_version


class AssetVersionKeyValue(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_version_key_value'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetVersionKeyValue',
    }

    key_id = Column(
        'key_id',
        Integer,
        ForeignKey('key.id'),
        primary_key=True,
    )

    value_id = Column(
        'value_id',
        Integer,
        ForeignKey('value.id'),
        primary_key=True,
    )

    asset_version_id = Column(
        'asset_version_id',
        Integer,
        ForeignKey('asset_version.id'),
        primary_key=True,
    )

    key = relationship('Key')

    value = relationship('Value')

    asset_version = relationship('AssetVersion')

    def __init__(self, key, value, asset_version):
        super(AssetVersionKeyValue, self).__init__()
        self.key = key
        self.value = value
        self.asset_version = asset_version


class AssetVersionDependency(base.Base, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_version_dependency'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetVersionDependency',
    }

    source_id = Column(
        'source_id',
        Integer,
        ForeignKey('asset_version.id'),
        primary_key=True,
    )

    destination_id = Column(
        'destination_id',
        Integer,
        ForeignKey('asset_version.id'),
        primary_key=True,
        autoincrement=True,
    )

    source = relationship(
        AssetVersion,
        primaryjoin='AssetVersionDependency.source_id==AssetVersion.id',
        backref='source_connections'
    )

    destination = relationship(
        AssetVersion,
        primaryjoin='AssetVersionDependency.destination_id==AssetVersion.id',
        backref='destination_connections'
    )

    def __init__(self, src_asset_version, dst_asset_version):
        super(AssetVersionDependency, self).__init__()
        self.source = src_asset_version
        self.destination = dst_asset_version

