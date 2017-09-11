"""
Shot tables.
"""

from sqlalchemy import (
    Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import relationship
from assetDB.models import modelbase as base
from assetDB.models import mixins


class ShotStatus(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'shot_status'
    __mapper_args__ = {
        'polymorphic_identity': 'ShotStatus',
    }

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
        super(ShotStatus, self).__init__()
        self._setKeywordFields(**kwargs)


class ShotCategory(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'shot_category'
    __mapper_args__ = {
        'polymorphic_identity': 'ShotCategory',
    }

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
        super(ShotCategory, self).__init__()
        self._setKeywordFields(**kwargs)


class Shot(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'shot'
    __mapper_args__ = {
        'polymorphic_identity': 'Shot'
    }
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }

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
        primaryjoin='Shot.config_file_id==ConfigFile.id',
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
        primaryjoin='Shot.shot_status_id==ShotStatus.id',
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
        primaryjoin='Shot.shot_category_id==ShotCategory.id',
    )

    project = relationship(
        'Project',
        secondary='sequence',
        primaryjoin='Shot.sequence_id==Sequence.id',
        secondaryjoin='Sequence.project_id==Project.id',
        uselist=False,
        viewonly=True,
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
        primaryjoin='Shot.sequence_id==Sequence.id'
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
        primaryjoin='Shot.scene_id==Scene.id'
    )

    tasks = relationship(
        'Task',
        primaryjoin='Shot.id==Task.shot_id'
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
    
    shot_range_start = Column('shot_range_start', Integer, nullable=True)
    shot_range_end = Column('shot_range_end', Integer, nullable=True)

    cut_range_start = Column('cut_range_start', Integer, nullable=True)
    cut_range_end = Column('cut_range_end', Integer, nullable=True)

    render_range_start = Column('render_range_start', Integer, nullable=True)
    render_range_end = Column('render_range_end', Integer, nullable=True)
    
    cache_range_start = Column('cache_range_start', Integer, nullable=True)
    cache_range_end = Column('cache_range_end', Integer, nullable=True)

    def __init__(self, **kwargs):
        super(Shot, self).__init__()
        self._setKeywordFields(**kwargs)
