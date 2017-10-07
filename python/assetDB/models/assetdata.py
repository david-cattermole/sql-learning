"""
Asset Data database tables

TODO: Add the ability for an AssetData class to have a thumbnail.
"""
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship

from assetDB.models import mixins
from assetDB.models import modelbase as base


class AssetDataStatus(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_data_status'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataStatus',
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
        nullable=False,
        unique=True,
    )

    description = Column(
        'description',
        String(base.DESCRIPTION_LENGTH),
        nullable=True,
    )

    asset_datas = relationship('AssetData')

    def __init__(self, **kwargs):
        super(AssetDataStatus, self).__init__()
        self._setKeywordFields(**kwargs)


class AssetDataName(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_data_name'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataName',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    asset_datas = relationship('AssetData')

    def __init__(self, **kwargs):
        super(AssetDataName, self).__init__()
        self._setKeywordFields(**kwargs)


class AssetDataSubname(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_data_subname'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataSubname',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    asset_datas = relationship('AssetData')

    def __init__(self, **kwargs):
        super(AssetDataSubname, self).__init__()
        self._setKeywordFields(**kwargs)


class AssetDataVariant(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_data_variant'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataVariant',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    asset_datas = relationship('AssetData')

    def __init__(self, **kwargs):
        super(AssetDataVariant, self).__init__()
        self._setKeywordFields(**kwargs)


class AssetDataResolution(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_data_resolution'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataResolution',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    asset_datas = relationship('AssetData')

    def __init__(self, **kwargs):
        super(AssetDataResolution, self).__init__()
        self._setKeywordFields(**kwargs)


class AssetDataInstance(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_data_instance'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataInstance',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    asset_datas = relationship('AssetData')

    def __init__(self, **kwargs):
        super(AssetDataInstance, self).__init__()
        self._setKeywordFields(**kwargs)


class AssetDataType(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_data_type'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataType',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    asset_datas = relationship('AssetData')

    def __init__(self, **kwargs):
        super(AssetDataType, self).__init__()
        self._setKeywordFields(**kwargs)


class AssetData(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_data'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetData',
    }

    shot_id = Column(
        'shot_id', Integer,
        ForeignKey('shot.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True
    )

    asset_id = Column(
        'asset_id', Integer,
        ForeignKey('asset.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True
    )

    asset_data_status_id = Column(
        'asset_data_status_id',
        Integer,
        ForeignKey(
            'asset_data_status.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    asset_data_status = relationship(
        'AssetDataStatus',
        foreign_keys=[asset_data_status_id]
    )

    asset_data_name_id = Column(
        'asset_data_name_id',
        Integer,
        ForeignKey('asset_data_name.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=False,
        unique=False,
    )

    asset_data_subname_id = Column(
        'asset_data_subname_id',
        Integer,
        ForeignKey('asset_data_subname.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    asset_data_variant_id = Column(
        'asset_data_variant_id',
        Integer,
        ForeignKey('asset_data_variant.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    asset_data_type_id = Column(
        'asset_data_type_id',
        Integer,
        ForeignKey('asset_data_type.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    asset_data_resolution_id = Column(
        'asset_data_resolution_id',
        Integer,
        ForeignKey('asset_data_resolution.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    asset_data_instance_id = Column(
        'asset_data_instance_id',
        Integer,
        ForeignKey('asset_data_instance.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    shot = relationship('Shot')

    asset = relationship('Asset')

    asset_data_name = relationship('AssetDataName')

    asset_data_subname = relationship('AssetDataSubname')

    asset_data_variant = relationship('AssetDataVariant')

    asset_data_type = relationship('AssetDataType')

    asset_data_resolution = relationship('AssetDataResolution')

    asset_data_instance = relationship('AssetDataInstance')

    asset_data_versions = relationship('AssetDataVersion')

    def __init__(self, **kwargs):
        super(AssetData, self).__init__()
        self._setKeywordFields(**kwargs)


class AssetDataVersion(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_data_version'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataVersion',
    }
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }

    asset_data_id = Column(
        'asset_data_id', Integer,
        ForeignKey('asset_data.id', onupdate='CASCADE', ondelete='CASCADE'),
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

    revision = Column(
        'revision',
        Integer,
        nullable=False,
        unique=False,
    )

    approved = Column(
        'approved',
        Boolean,
        nullable=False,
        unique=False,
    )

    frozen = Column(
        'frozen',
        Boolean,
        nullable=False,
        unique=False,
    )

    asset_data = relationship('AssetData')

    media_version = relationship('MediaVersion')

    task = relationship('Task')

    def __init__(self, **kwargs):
        super(AssetDataVersion, self).__init__()
        self._setKeywordFields(**kwargs)


class AssetDataDependency(base.Base, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_data_dependency'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataDependency',
    }

    source_id = Column(
        Integer,
        ForeignKey('asset_data.id'),
        primary_key=True,
    )

    destination_id = Column(
        Integer,
        ForeignKey('asset_data.id'),
        primary_key=True,
        autoincrement=True,
    )

    source_asset_data = relationship(
        AssetData,
        primaryjoin='AssetDataDependency.source_id==AssetData.id',
        backref='source_connections'
    )

    destination_asset_data = relationship(
        AssetData,
        primaryjoin='AssetDataDependency.destination_id==AssetData.id',
        backref='destination_connections'
    )

    def __init__(self, src_asset_data, dst_asset_data):
        super(AssetDataDependency, self).__init__()
        self.source_asset_data = src_asset_data
        self.destination_asset_data = dst_asset_data
