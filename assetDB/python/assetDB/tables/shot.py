"""
Shot tables.
"""

from sqlalchemy import (
    Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import relationship
from assetDB.tables import tablebase as base


class ShotStatus(base.Base):
    __tablename__ = 'shot_status'
    __mapper_args__ = {
        'polymorphic_identity': 'ShotStatus',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    shots = relationship('Shot')

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


class ShotCategory(base.Base):
    __tablename__ = 'shot_category'
    __mapper_args__ = {
        'polymorphic_identity': 'ShotCategory',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    shots = relationship('Shot')

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


class Shot(base.Base):
    __tablename__ = 'shot'
    __mapper_args__ = {
        'polymorphic_identity': 'Shot'
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

    shot_status_id = Column(
        'shot_status_id',
        Integer,
        ForeignKey(
            'shot_status.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    shot_status = relationship(
        'ShotStatus',
        foreign_keys=[shot_status_id]
    )

    shot_category_id = Column(
        'shot_category_id',
        Integer,
        ForeignKey(
            'shot_category.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    shot_category = relationship(
        'ShotCategory',
        foreign_keys=[shot_category_id]
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

    sequence_id = Column(
        'sequence_id',
        Integer,
        ForeignKey(
            'sequence.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    sequence = relationship(
        'Sequence',
        foreign_keys=[sequence_id]
    )

    scene_id = Column(
        'scene_id',
        Integer,
        ForeignKey(
            'scene.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=True,
        unique=False,
    )

    scene = relationship(
        'Scene',
        foreign_keys=[scene_id]
    )

    tasks = relationship('Task')

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
    
    shot_range_start = Column('shot_range_start', Integer, nullable=True)
    shot_range_end = Column('shot_range_end', Integer, nullable=True)

    cut_range_start = Column('cut_range_start', Integer, nullable=True)
    cut_range_end = Column('cut_range_end', Integer, nullable=True)

    render_range_start = Column('render_range_start', Integer, nullable=True)
    render_range_end = Column('render_range_end', Integer, nullable=True)
    
    cache_range_start = Column('cache_range_start', Integer, nullable=True)
    cache_range_end = Column('cache_range_end', Integer, nullable=True)

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)
