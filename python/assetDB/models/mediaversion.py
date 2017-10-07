"""
Media version database tables. 
"""

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from assetDB.models import mixins
from assetDB.models import modelbase as base


class ImageResolution(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'image_resolution'
    __mapper_args__ = {
        'polymorphic_identity': 'ImageResolutionEntity',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    width = Column(
        'width',
        Integer,
        nullable=False,
    )

    height = Column(
        'height',
        Integer,
        nullable=False,
    )

    pixel_aspect = Column(
        'pixel_aspect',
        Numeric,
        nullable=False,
    )

    def __init__(self, **kwargs):
        super(ImageResolution, self).__init__()
        self._setKeywordFields(**kwargs)


class MediaVersionName(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'media_version_name'
    __mapper_args__ = {
        'polymorphic_identity': 'MediaVersionName',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(MediaVersionName, self).__init__()
        self._setKeywordFields(**kwargs)


class MediaVersionSubname(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'media_version_subname'
    __mapper_args__ = {
        'polymorphic_identity': 'MediaVersionSubname',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(MediaVersionSubname, self).__init__()
        self._setKeywordFields(**kwargs)


class MediaVersionCategory(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'media_version_category'
    __mapper_args__ = {
        'polymorphic_identity': 'MediaVersionCategory',
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

    media_versions = relationship('MediaVersion')

    def __init__(self, **kwargs):
        super(MediaVersionCategory, self).__init__()
        self._setKeywordFields(**kwargs)


class MediaVersionStatus(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'media_version_status'
    __mapper_args__ = {
        'polymorphic_identity': 'MediaVersionStatus',
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

    media_versions = relationship('MediaVersion')

    def __init__(self, **kwargs):
        super(MediaVersionStatus, self).__init__()
        self._setKeywordFields(**kwargs)


class MediaVersion(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'media_version'
    __mapper_args__ = {
        'polymorphic_identity': 'MediaVersion',
    }

    media_version_status_id = Column(
        'media_version_status_id',
        Integer,
        ForeignKey(
            'media_version_status.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    media_version_category_id = Column(
        'media_version_category_id',
        Integer,
        ForeignKey(
            'media_version_category.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    media_version_name_id = Column(
        'media_version_name_id',
        Integer,
        ForeignKey(
            'media_version_name.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )
    
    media_version_subname_id = Column(
        'media_version_subname_id',
        Integer,
        ForeignKey(
            'media_version_subname.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=True,
        unique=False,
    )

    task_id = Column(
        'task_id',
        Integer,
        ForeignKey(
            'task.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    image_resolution_id = Column(
        'image_resolution_id',
        Integer,
        ForeignKey(
            'image_resolution.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
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

    image_resolution = relationship(
        'ImageResolution'
    )

    media_version_name = relationship(
        'MediaVersionName',
        foreign_keys=[media_version_name_id]
    )

    media_version_subname = relationship(
        'MediaVersionSubname',
        foreign_keys=[media_version_subname_id]
    )

    media_version_status = relationship(
        'MediaVersionStatus',
        foreign_keys=[media_version_status_id]
    )
    
    media_version_category = relationship(
        'MediaVersionCategory',
        foreign_keys=[media_version_category_id]
    )

    task = relationship('Task')

    def __init__(self, **kwargs):
        super(MediaVersion, self).__init__()
        self._setKeywordFields(**kwargs)
