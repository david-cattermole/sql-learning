from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship

from assetDB.tables import tablebase as base


class AssetDataStatus(base.Base):
    __tablename__ = 'asset_data_status'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataStatus',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # asset_data = relationship('AssetData')

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

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self._setKeywordFields(**kwargs)


class AssetDataName(base.Base):
    __tablename__ = 'asset_data_name'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataName',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # asset_datas = relationship('AssetData')

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class AssetDataSubname(base.Base):
    __tablename__ = 'asset_data_subname'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataSubname',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # asset_datas = relationship('AssetData')

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class AssetDataVariant(base.Base):
    __tablename__ = 'asset_data_variant'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataVariant',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # asset_datas = relationship('AssetData')

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class AssetDataResolution(base.Base):
    __tablename__ = 'asset_data_resolution'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataResolution',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # asset_datas = relationship('AssetData')

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class AssetDataInstance(base.Base):
    __tablename__ = 'asset_data_instance'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataInstance',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # asset_datas = relationship('AssetData')

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class AssetDataType(base.Base):
    __tablename__ = 'asset_data_type'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataType',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # asset_datas = relationship('AssetData')

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class AssetData(base.Base):
    __tablename__ = 'asset_data'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetData',
    }
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
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

    # @declared_attr
    # def keyvalues(cls):
    #     return relationship(
    #         "KeyValue",
    #         secondary=keyvalue_assetdata_table,
    #     )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class AssetDataVersion(base.Base):
    __tablename__ = 'asset_data_version'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetDataVersion',
    }
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    asset_data_id = Column(
        'asset_data_id', Integer,
        ForeignKey('asset_data.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )

    asset_data = relationship('AssetData')

    media_id = Column(
        'media_id', Integer,
        ForeignKey('media.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True
    )

    media = relationship('Media')

    task_id = Column(
        'task_id', Integer,
        ForeignKey('task.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True
    )

    task = relationship('Task')

    code = Column(
        'code',
        String(base.CODE_LENGTH),
        nullable=False,
        unique=True,
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

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class AssetDataDependency(base.Base):
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

    def __init__(self, asset_data1, asset_data2):
        self.source_asset_data = asset_data1
        self.destination_asset_data = asset_data2
