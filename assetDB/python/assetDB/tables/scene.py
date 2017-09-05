"""
Scene tables.
"""

from sqlalchemy import (
    Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import relationship
from assetDB.tables import tablebase as base


class SceneStatus(base.Base):
    __tablename__ = 'scene_status'
    __mapper_args__ = {
        'polymorphic_identity': 'SceneStatus',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    scenes = relationship('Scene')

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


class SceneCategory(base.Base):
    __tablename__ = 'scene_category'
    __mapper_args__ = {
        'polymorphic_identity': 'SceneCategory',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    scenes = relationship('Scene')

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


class Scene(base.Base):
    __tablename__ = 'scene'
    __mapper_args__ = {
        'polymorphic_identity': 'Scene'
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

    scene_status_id = Column(
        'scene_status_id',
        Integer,
        ForeignKey(
            'scene_status.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    scene_status = relationship(
        'SceneStatus',
        foreign_keys=[scene_status_id]
    )

    scene_category_id = Column(
        'scene_category_id',
        Integer,
        ForeignKey(
            'scene_category.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    scene_category = relationship(
        'SceneCategory',
        foreign_keys=[scene_category_id]
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

    shots = relationship('Shot')

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

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)
