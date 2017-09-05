from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from assetDB.tables import tablebase as base


class ImageResolution(base.Base):
    __tablename__ = 'image_resolution'
    __mapper_args__ = {
        'polymorphic_identity': 'ImageResolution',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

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
        super(self.__class__, self).__init__()
        self._setKeywordFields(**kwargs)


class MediaVersionStatus(base.Base):
    __tablename__ = 'media_status'
    __mapper_args__ = {
        'polymorphic_identity': 'MediaVersionStatus',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    media_versions = relationship('MediaVersion')

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


class Media(base.Base):
    __tablename__ = 'media'
    __mapper_args__ = {
        'polymorphic_identity': 'Media',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=False,
    )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self._setKeywordFields(**kwargs)


class MediaVersion(base.Base):
    __tablename__ = 'media_version'
    __mapper_args__ = {
        'polymorphic_identity': 'MediaVersion',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    
    media_id = Column(
        'media_id',
        Integer,
        ForeignKey(
            'media.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    media = relationship(
        'Media',
        foreign_keys=[media_id]
    )

    media_version_status_id = Column(
        'media_version_status_id',
        Integer,
        ForeignKey(
            'media_status.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    media_version_status = relationship(
        'MediaVersionStatus',
        foreign_keys=[media_version_status_id]
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

    task = relationship('Task')

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

    image_resolution = relationship('ImageResolution')

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

    # approved = Column(
    #     'approved',
    #     Boolean,
    #     nullable=True,
    #     unique=False,
    # )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self._setKeywordFields(**kwargs)
