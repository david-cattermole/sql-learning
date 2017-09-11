from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from assetDB.models import modelbase as base
from assetDB.models import mixins


class OperatingSystem(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'operating_system'
    __mapper_args__ = {
        'polymorphic_identity': 'OperatingSystem',
    }

    storage_roots = relationship('StorageRoot')

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(OperatingSystem, self).__init__()
        self._setKeywordFields(**kwargs)


class StorageRoot(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'storage_root'
    __mapper_args__ = {
        'polymorphic_identity': 'StorageRoot',
    }

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

    operating_system_id = Column(
        'operating_system_id',
        Integer,
        ForeignKey(
            'operating_system.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        unique=False,
    )

    operating_system = relationship(
        'OperatingSystem',
        foreign_keys=[operating_system_id]
    )

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    description = Column(
        'description',
        String(base.DESCRIPTION_LENGTH),
        nullable=True,
        unique=True,
    )

    root_path = Column(
        'root_path',
        String(255),
        nullable=False,
        unique=False,
    )

    def __init__(self, **kwargs):
        super(StorageRoot, self).__init__()
        self._setKeywordFields(**kwargs)


class ProjectStatus(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'project_status'
    __mapper_args__ = {
        'polymorphic_identity': 'ProjectStatus',
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

    # projects = relationship('Project')

    def __init__(self, **kwargs):
        super(ProjectStatus, self).__init__()
        self._setKeywordFields(**kwargs)


class ProjectCategory(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'project_category'
    __mapper_args__ = {
        'polymorphic_identity': 'ProjectCategory',
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
        unique=True,
    )

    description = Column(
        'description',
        String(base.DESCRIPTION_LENGTH),
        nullable=True,
    )

    # projects = relationship('Project')

    def __init__(self, **kwargs):
        super(ProjectCategory, self).__init__()
        self._setKeywordFields(**kwargs)


class Project(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'project'
    __mapper_args__ = {
        'polymorphic_identity': 'Project',
    }

    project_status_id = Column(
        'project_status_id',
        Integer,
        ForeignKey('project_status.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        unique=False,
    )

    project_category_id = Column(
        'project_category_id',
        Integer,
        ForeignKey('project_category.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=False,
        unique=False,
    )

    project_status = relationship(
        'ProjectStatus',
        backref='projects'
    )

    project_category = relationship(
        'ProjectCategory',
        backref='projects'
    )

    storage_roots = relationship(
        'StorageRoot',
    )

    config_file_id = Column(
        'config_file_id',
        Integer,
        ForeignKey('config_file.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    config_file = relationship('ConfigFile')

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
        unique=False,
    )

    # # TODO: Implement 'keyvalues' (tags).
    # keyvalues = relationship(
    #         "KeyValue",
    #         secondary=keyvalue_project_table,
    #     )

    def __init__(self, **kwargs):
        super(Project, self).__init__()
        self._setKeywordFields(**kwargs)
