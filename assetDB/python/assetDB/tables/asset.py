"""
Asset table.
"""

from sqlalchemy import (
    Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import relationship
from assetDB.tables import tablebase as base


class AssetStatus(base.Base):
    __tablename__ = 'asset_status'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetStatus',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    assets = relationship('Asset')

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


class AssetCategory(base.Base):
    __tablename__ = 'asset_category'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetCategory',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # assets = relationship('AssetStatus')

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

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self._setKeywordFields(**kwargs)


class Asset(base.Base):
    __tablename__ = 'asset'
    __mapper_args__ = {
        'polymorphic_identity': 'Asset',
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

    asset_status_id = Column(
        'asset_status_id',
        Integer,
        ForeignKey(
            'asset_status.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    asset_status = relationship(
        'AssetStatus',
        foreign_keys=[asset_status_id]
    )

    asset_category_id = Column(
        'asset_category_id',
        Integer,
        ForeignKey(
            'asset_category.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    asset_category = relationship(
        'AssetCategory',
        foreign_keys=[asset_category_id]
    )

    project_id = Column(
        'project_id',
        Integer,
        ForeignKey(
            'project.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    project = relationship(
        'Project',
        foreign_keys=[project_id]
    )

    config_file_id = Column(
        'config_file_id',
        Integer,
        ForeignKey(
            'config_file.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=True,
        unique=False,
    )

    config_file = relationship(
        'ConfigFile',
        foreign_keys=[config_file_id]
    )

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=False,
    )

    description = Column(
        'description',
        String(base.DESCRIPTION_LENGTH),
        nullable=True,
    )

    # asset_datas = relationship('AssetData')

    # created_datetime = Column(
    #     'created_datetime',
    #     DateTime,
    #     default=datetime.datetime.utcnow(),
    # )
    #
    # created_user_id = Column(
    #     'created_user_id',
    #     ForeignKey('user.id'),
    #     nullable=True,
    #     default=setup.get_current_user,
    # )
    #
    # created_site_id = Column(
    #     'created_site_id',
    #     ForeignKey('site.id'),
    #     default=setup.get_current_site,
    #     nullable=True,
    # )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)
