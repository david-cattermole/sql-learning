"""
Asset table.
"""

import uuid
from sqlalchemy import (
    Column, Integer, String, ForeignKey
)
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from assetDB.models import modelbase as base
from assetDB.models import mixins


class AssetStatus(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_status'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetStatus',
    }

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
        super(AssetStatus, self).__init__()
        self._setKeywordFields(**kwargs)


class AssetCategory(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset_category'
    __mapper_args__ = {
        'polymorphic_identity': 'AssetCategory',
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

    # assets = relationship('AssetStatus')

    def __init__(self, **kwargs):
        super(AssetCategory, self).__init__()
        self._setKeywordFields(**kwargs)


class Asset(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'asset'
    __mapper_args__ = {
        'polymorphic_identity': 'Asset',
    }
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }

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

    def __init__(self, **kwargs):
        super(AssetCategory, self).__init__()
        self._setKeywordFields(**kwargs)
