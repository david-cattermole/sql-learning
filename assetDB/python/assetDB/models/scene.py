"""
Scene tables.
"""

from sqlalchemy import (
    Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import relationship
from assetDB.models import modelbase as base
from assetDB.models import mixins


class SceneStatus(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'scene_status'
    __mapper_args__ = {
        'polymorphic_identity': 'SceneStatus',
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

    scenes = relationship('Scene')

    def __init__(self, **kwargs):
        super(SceneStatus, self).__init__()
        self._setKeywordFields(**kwargs)


class SceneCategory(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'scene_category'
    __mapper_args__ = {
        'polymorphic_identity': 'SceneCategory',
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

    scenes = relationship('Scene')

    def __init__(self, **kwargs):
        super(SceneCategory, self).__init__()
        self._setKeywordFields(**kwargs)


class Scene(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'scene'
    __mapper_args__ = {
        'polymorphic_identity': 'Scene'
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

    shots = relationship(
        'Shot',
        primaryjoin='Scene.id==Shot.scene_id'
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

    def __init__(self, **kwargs):
        super(Scene, self).__init__()
        self._setKeywordFields(**kwargs)
