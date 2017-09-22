"""
Asset Data database tables
"""
import os

from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship

from assetDB.models import mixins
from assetDB.models import modelbase as base


class Asset(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset'
    __mapper_args__ = {
        'polymorphic_identity': 'Asset',
    }

    project_id = Column(
        'project_id',
        Integer,
        ForeignKey('project.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=False,
        unique=False,
    )

    sequence_id = Column(
        'sequence_id',
        Integer,
        ForeignKey('sequence.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=False,
        unique=False,
    )

    shot_id = Column(
        'shot_id',
        Integer,
        ForeignKey('shot.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=False,
        unique=False,
    )

    name_id = Column(
        'name_id',
        Integer,
        ForeignKey('name.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=False,
        unique=False,
    )

    subname_id = Column(
        'subname_id',
        Integer,
        ForeignKey('subname.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    variant_id = Column(
        'variant_id',
        Integer,
        ForeignKey('variant.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    type_id = Column(
        'type_id',
        Integer,
        ForeignKey('type.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    resolution_id = Column(
        'resolution_id',
        Integer,
        ForeignKey('resolution.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    instance_id = Column(
        'instance_id',
        Integer,
        ForeignKey('instance.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    project = relationship('Project')

    sequence = relationship('Sequence')

    shot = relationship('Shot')

    name = relationship('Name')

    subname = relationship('Subname')

    variant = relationship('Variant')

    type = relationship('Type')

    resolution = relationship('Resolution')

    instance = relationship('Instance')

    asset_versions = relationship('AssetVersion')

    tags = relationship(
        'Tag',
        secondary='asset_tag',
    )

    key_values = relationship(
        'AssetKeyValue',
        secondary='asset_key_value',
        secondaryjoin='AssetKeyValue.asset_id==Asset.id',
    )

    def __init__(self, **kwargs):
        super(Asset, self).__init__()
        self._setKeywordFields(**kwargs)

    def get_path(self):
        project = self.project.name
        sequence = self.sequence.name
        shot = self.shot.name
        name = self.name.name
        subname = self.subname.name
        variant = self.variant.name
        instance = self.instance.name
        resolution = self.resolution.name
        type = self.type.name

        path = os.path.join(
            os.path.sep,
            project, sequence, shot,
            name, subname, instance,
            variant, resolution, type)
        return path

    path = property(get_path)


class AssetTag(base.Base, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_tag'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetTag',
    }

    tag_id = Column(
        'tag_id',
        Integer,
        ForeignKey('tag.id'),
        primary_key=True,
        autoincrement=True,
    )

    asset_id = Column(
        'asset_id',
        Integer,
        ForeignKey('asset.id'),
        primary_key=True,
    )

    tag = relationship('Tag')

    asset = relationship('Asset')

    def __init__(self, tag, asset):
        super(AssetTag, self).__init__()
        self.tag = tag
        self.asset = asset


class AssetKeyValue(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_key_value'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetKeyValue',
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

    asset_id = Column(
        'asset_id',
        Integer,
        ForeignKey('asset.id'),
        primary_key=True,
    )

    key = relationship('Key')

    value = relationship('Value')

    asset = relationship('Asset')

    def __init__(self, key, value, asset):
        super(AssetKeyValue, self).__init__()
        self.key = key
        self.value = value
        self.asset = asset


class AssetDependency(base.Base, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_dependency'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDependency',
    }

    source_id = Column(
        Integer,
        ForeignKey('asset.id'),
        primary_key=True,
    )

    destination_id = Column(
        Integer,
        ForeignKey('asset.id'),
        primary_key=True,
        autoincrement=True,
    )

    source = relationship(
        Asset,
        primaryjoin='AssetDependency.source_id==Asset.id',
        backref='source_connections'
    )

    destination = relationship(
        Asset,
        primaryjoin='AssetDependency.destination_id==Asset.id',
        backref='destination_connections'
    )

    def __init__(self, src_asset, dst_asset):
        super(AssetDependency, self).__init__()
        self.source = src_asset
        self.destination = dst_asset

