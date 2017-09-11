"""
Sequence tables.
"""

from sqlalchemy import (
    Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import relationship
from assetDB.models import modelbase as base
from assetDB.models import mixins


class SequenceStatus(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'sequence_status'
    __mapper_args__ = {
        'polymorphic_identity': 'SequenceStatus',
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

    sequences = relationship(
        'Sequence',
        primaryjoin='SequenceStatus.id==Sequence.sequence_status_id'
    )

    def __init__(self, **kwargs):
        super(SequenceStatus, self).__init__()
        self._setKeywordFields(**kwargs)


class SequenceCategory(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'sequence_category'
    __mapper_args__ = {
        'polymorphic_identity': 'SequenceCategory',
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

    sequences = relationship(
        'Sequence',
        primaryjoin='SequenceCategory.id==Sequence.sequence_category_id'
    )

    def __init__(self, **kwargs):
        super(SequenceCategory, self).__init__()
        self._setKeywordFields(**kwargs)


class Sequence(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'sequence'
    __mapper_args__ = {
        'polymorphic_identity': 'Sequence'
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

    sequence_status_id = Column(
        'sequence_status_id',
        Integer,
        ForeignKey(
            'sequence_status.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    sequence_status = relationship(
        'SequenceStatus',
        foreign_keys=[sequence_status_id]
    )

    sequence_category_id = Column(
        'sequence_category_id',
        Integer,
        ForeignKey(
            'sequence_category.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    sequence_category = relationship(
        'SequenceCategory',
        foreign_keys=[sequence_category_id]
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
        primaryjoin='Sequence.project_id==Project.id'
    )

    shots = relationship(
        'Shot',
        primaryjoin='Sequence.id==Shot.sequence_id'
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
        super(Sequence, self).__init__()
        self._setKeywordFields(**kwargs)
