from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from assetDB.tables import tablebase as base


class OperatingSystem(base.Base):
    __tablename__ = 'operating_system'
    __mapper_args__ = {
        'polymorphic_identity': 'OperatingSystem',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    storage_roots = relationship('StorageRoot')

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self._setKeywordFields(**kwargs)


class StorageRoot(base.Base):
    __tablename__ = 'storage_root'
    __mapper_args__ = {
        'polymorphic_identity': 'StorageRoot',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
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
        super(self.__class__, self).__init__()
        self._setKeywordFields(**kwargs)


class ProjectStatus(base.Base):
    __tablename__ = 'project_status'
    __mapper_args__ = {
        'polymorphic_identity': 'ProjectStatus',
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
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class ProjectCategory(base.Base):
    __tablename__ = 'project_category'
    __mapper_args__ = {
        'polymorphic_identity': 'ProjectCategory',
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
        super(self.__class__, self).__init__()
        self._setKeywordFields(**kwargs)


class Project(base.Base):
    __tablename__ = 'project'
    __mapper_args__ = {
        'polymorphic_identity': 'Project',
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

    # keyvalues = relationship(
    #         "KeyValue",
    #         secondary=keyvalue_project_table,
    #     )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)
