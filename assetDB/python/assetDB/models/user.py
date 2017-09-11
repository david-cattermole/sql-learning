"""
User table.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from assetDB.models import mixins
from assetDB.models import modelbase as base


class Site(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'site'
    __mapper_args__ = {
        'polymorphic_identity': 'site',
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

    address = Column(
        'address',
        String(255),
        nullable=True,
    )

    domain = Column(
        'domain',
        String(255),
        nullable=True,
    )

    users = relationship(
        'User',
        back_populates='site',
        primaryjoin='Site.id==User.site_id',
    )

    tasks = relationship(
        'Task',
        back_populates='site',
        primaryjoin='Site.id==Task.site_id'
    )

    def validate_name(self, value):
        if value is None:
            msg = "Keyword argument 'name' type must be str, not None, got %r"
            raise TypeError(msg % value)
        if not isinstance(value, basestring):
            msg = "Keyword argument 'name' type must be str or unicode, got %r"
            raise TypeError(msg % value)
        if not value.islower():
            msg = "Keyword argument 'name' must be lower-case only, got %r"
            raise TypeError(msg % value)
        return value

    def __init__(self, **kwargs):
        super(Site, self).__init__()
        kwargs['name'] = self.validate_name(kwargs.get('name'))
        self._setKeywordFields(**kwargs)


class Department(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'department'
    __mapper_args__ = {
        'polymorphic_identity': 'department',
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

    users = relationship(
        'User',
        primaryjoin='Department.id==User.department_id'
    )

    def __init__(self, **kwargs):
        super(Department, self).__init__()
        self._setKeywordFields(**kwargs)


class UserStatus(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'user_status'
    __mapper_args__ = {
        'polymorphic_identity': 'UserStatus',
    }

    users = relationship(
        'User',
        primaryjoin='UserStatus.id==User.user_status_id'
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
        unique=False,
    )

    description = Column(
        'description',
        String(base.DESCRIPTION_LENGTH),
        nullable=True,
    )

    def __init__(self, **kwargs):
        super(UserStatus, self).__init__()
        self._setKeywordFields(**kwargs)


class User(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'user'
    __mapper_args__ = {
        'polymorphic_identity': 'User',
    }

    # many to many 'UserGroup <-> User'
    user_groups = relationship(
        'UserGroup',
        secondary='user_group_to_user',
        back_populates='users',
        primaryjoin='User.id==UserGroupToUser.user_id',
        secondaryjoin='UserGroupToUser.user_group_id==UserGroup.id'
    )

    department_id = Column(
        'department_id',
        Integer,
        ForeignKey('department.id',
                   name='fk_department_id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    department = relationship(
        'Department',
        primaryjoin='User.department_id==Department.id'
    )

    site_id = Column(
        'site_id',
        Integer,
        ForeignKey('site.id',
                   name='fk_site_id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=True,
        unique=False,
    )

    site = relationship(
        'Site',
        primaryjoin='User.site_id==Site.id',
        back_populates='users'
    )
    
    user_status_id = Column(
        'user_status_id',
        Integer,
        ForeignKey('user_status.id',
                   name='fk_user_status_id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
        nullable=False,
        unique=False,
    )

    user_status = relationship(
        'UserStatus',
        primaryjoin='User.user_status_id==UserStatus.id',
        back_populates='users'
    )

    user_name = Column(
        'user_name',
        String(base.NAME_LENGTH),
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
        super(User, self).__init__()
        self._setKeywordFields(**kwargs)


class UserGroup(base.Base, mixins.IdentityMixin, mixins.CreatedUpdatedMixin):
    __tablename__ = 'user_group'
    __mapper_args__ = {
        'polymorphic_identity': 'UserGroup',
    }

    # many to many 'UserGroup <-> User'
    users = relationship(
        'User',
        secondary='user_group_to_user',
        primaryjoin='UserGroup.id==UserGroupToUser.user_group_id',
        secondaryjoin='UserGroupToUser.user_id==User.id'
        # back_populates='user_groups'
    )

    parent_id = Column(
        'parent_id',
        Integer,
        ForeignKey('user_group.id',
                   name='fk_parent_id',
                   onupdate='CASCADE',
                   ondelete='CASCADE'),
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
        backref=backref("parent", remote_side='UserGroup.id'),

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
        super(UserGroup, self).__init__()
        self._setKeywordFields(**kwargs)


class UserGroupToUser(base.Base, mixins.CreatedUpdatedMixin):
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


