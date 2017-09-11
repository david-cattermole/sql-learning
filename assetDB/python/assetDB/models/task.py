"""
Task table.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from assetDB.models import modelbase as base
from assetDB.models import mixins


class TaskStatus(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'task_status'
    __mapper_args__ = {
        'polymorphic_identity': 'TaskStatus',
    }

    tasks = relationship('Task')

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
        unique=False,
    )

    description = Column(
        'description',
        String(base.DESCRIPTION_LENGTH),
        nullable=True,
    )

    def __init__(self, **kwargs):
        super(TaskStatus, self).__init__()
        self._setKeywordFields(**kwargs)


class TaskCategory(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'task_category'
    __mapper_args__ = {
        'polymorphic_identity': 'TaskCategory',
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
        unique=False,
    )

    description = Column(
        'description',
        String(base.DESCRIPTION_LENGTH),
        nullable=True,
    )

    tasks = relationship('Task')

    def __init__(self, **kwargs):
        super(TaskCategory, self).__init__()
        self._setKeywordFields(**kwargs)


class Task(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'task'
    __mapper_args__ = {
        'polymorphic_identity': 'Task',
    }

    # many to many 'Task <-> User'
    users = relationship(
        'User',
        secondary='task_to_user',
        primaryjoin='Task.id==TaskToUser.task_id',
        secondaryjoin='TaskToUser.user_id==User.id'
    )

    def destination_neighbours(self):
        return [x.destination_task for x in self.source_connections]

    def source_neighbours(self):
        return [x.source_task for x in self.destination_connections]

    asset_id = Column(
        'asset_id',
        Integer,
        ForeignKey('asset.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    shot_id = Column(
        'shot_id',
        Integer,
        ForeignKey('shot.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    department_id = Column(
        'department_id',
        Integer,
        ForeignKey('department.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    site_id = Column(
        'site_id',
        Integer,
        ForeignKey('site.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )
    
    task_category_id = Column(
        'task_category_id',
        Integer,
        ForeignKey('task_category.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        unique=False,
    )

    task_status_id = Column(
        'task_status_id',
        Integer,
        ForeignKey('task_status.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        unique=False,
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
    )

    asset = relationship('Asset')

    shot = relationship('Shot')

    department = relationship('Department')

    site = relationship('Site', back_populates='tasks')

    task_status = relationship('TaskStatus', back_populates='tasks')

    task_category = relationship('TaskCategory', back_populates='tasks')
    
    date_ranges = relationship('TaskDateRange')

    def __init__(self, **kwargs):
        super(Task, self).__init__()
        self._setKeywordFields(**kwargs)


class TaskDependency(base.Base, mixins.CreatedUpdatedMixin):
    __tablename__ = 'task_dependency'
    __mapper_args__ = {
        'polymorphic_identity': 'TaskDependency',
    }

    source_id = Column(
        Integer,
        ForeignKey('task.id'),
        primary_key=True,
    )

    destination_id = Column(
        Integer,
        ForeignKey('task.id'),
        primary_key=True,
        autoincrement=True,
    )

    source_task = relationship(
        Task,
        primaryjoin='TaskDependency.source_id==Task.id',
        backref='source_connections'
    )

    destination_task = relationship(
        Task,
        primaryjoin='TaskDependency.destination_id==Task.id',
        backref='destination_connections'
    )

    def __init__(self, task1, task2):
        self.source_task = task1
        self.destination_task = task2


class TaskToUser(base.Base, mixins.CreatedUpdatedMixin):
    __tablename__ = 'task_to_user'
    __mapper_args__ = {
        'polymorphic_identity': 'TaskToUser',
    }

    task_id = Column(
        'task_id',
        Integer,
        ForeignKey('task.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        primary_key=True,
    )

    user_id = Column(
        'user_id',
        Integer,
        ForeignKey('user.id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        primary_key=True,
    )

    task = relationship(
        'Task',
        primaryjoin='TaskToUser.task_id==Task.id'
    )

    user = relationship(
        'User',
        primaryjoin='TaskToUser.user_id==User.id'
    )

    def __init__(self, task, user):
        self.task = task
        self.user = user


class TaskDateRange(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'task_date_range'
    __mapper_args__ = {
        'polymorphic_identity': 'TaskDateRange',
    }

    task_id = Column(
        'task_id',
        Integer,
        ForeignKey('task.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    task = relationship('Task')

    start = Column(
        'start',
        DateTime(timezone=True),
        nullable=False,
        unique=False,
    )

    end = Column(
        'end',
        DateTime(timezone=True),
        nullable=False,
        unique=False,
    )

    def __init__(self, **kwargs):
        super(TaskDateRange, self).__init__()
        self._setKeywordFields(**kwargs)
