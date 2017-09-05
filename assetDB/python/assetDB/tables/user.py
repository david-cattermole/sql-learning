"""
User table.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from assetDB.tables import tablebase as base


class Site(base.Base):
    __tablename__ = 'site'
    __mapper_args__ = {
        'polymorphic_identity': 'site',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    users = relationship('User', back_populates='site')

    tasks = relationship('Task', back_populates='site')

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

    address = Column(
        'address',
        String(255),
        nullable=True,
    )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class Department(base.Base):
    __tablename__ = 'department'
    __mapper_args__ = {
        'polymorphic_identity': 'department',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    users = relationship('User')

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

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class UserStatus(base.Base):
    __tablename__ = 'user_status'
    __mapper_args__ = {
        'polymorphic_identity': 'UserStatus',
    }

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    users = relationship('User')

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
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class User(base.Base):
    __tablename__ = 'user'
    __mapper_args__ = {
        'polymorphic_identity': 'User',
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

    # many to many 'UserGroup <-> User'
    user_groups = relationship(
        'UserGroup',
        secondary='user_group_to_user',
        back_populates='users'
    )

    department_id = Column(
        'department_id',
        Integer,
        ForeignKey('department.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    department = relationship('Department')

    site_id = Column(
        'site_id',
        Integer,
        ForeignKey('site.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    site = relationship('Site', back_populates='users')
    
    user_status_id = Column(
        'user_status_id',
        Integer,
        ForeignKey('user_status.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        unique=False,
    )

    user_status = relationship('UserStatus', back_populates='users')

    user_name = Column(
        'user_name',
        String(255),
        nullable=False,
        unique=True,
    )

    password = Column(
        'password',
        String(255),
        nullable=False,
    )

    first_name = Column(
        'first_name',
        String(255),
        nullable=True,
    )

    last_name = Column(
        'last_name',
        String(255),
        nullable=True,
    )

    nick_name = Column(
        'nick_name',
        String(255),
        nullable=True,
    )

    email_address = Column(
        'email_address',
        String(255),
        nullable=True,
    )

    phone_number = Column(
        'phone_number',
        String(255),
        nullable=True,
    )

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class UserGroup(base.Base):
    __tablename__ = 'user_group'
    __mapper_args__ = {
        'polymorphic_identity': 'UserGroup',
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

    # many to many 'UserGroup <-> User'
    users = relationship(
        'User',
        secondary='user_group_to_user',
        # back_populates='user_groups'
    )

    parent_id = Column(
        'parent_id',
        Integer,
        ForeignKey('user_group.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        unique=False
    )

    children = relationship(
        'UserGroup',
        # cascade deletions
        cascade='all, delete-orphan',

        # many to one + adjacency list - remote_side
        # is required to reference the 'remote'
        # column in the join condition.
        backref=backref("parent", remote_side=id),

        # children will be represented as a dictionary
        # on the "name" attribute.
        collection_class=attribute_mapped_collection('name'),
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

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__()
        self.code = base.getCode()
        self._setKeywordFields(**kwargs)


class UserGroupToUser(base.Base):
    __tablename__ = 'user_group_to_user'
    __mapper_args__ = {
        'polymorphic_identity': 'UserGroupToUser',
    }

    user_group_id = Column(
        'user_group_id',
        Integer,
        ForeignKey('user_group.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )

    user_id = Column(
        'user_id',
        Integer,
        ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )

    user_group = relationship(
        UserGroup,
        primaryjoin='UserGroupToUser.user_group_id==UserGroup.id',
    )

    user = relationship(
        User,
        primaryjoin='UserGroupToUser.user_id==User.id',
    )

    def __init__(self, user_group, user):
        self.user_group = user_group
        self.user = user
