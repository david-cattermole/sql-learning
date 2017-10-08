"""
File Data database tables
"""

from sqlalchemy import (
    Column, Integer, BigInteger, String, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

import mediaDB2.config as config
from mediaDB2.models import mixins
from mediaDB2.models import modelbase as base


class Repository(base.Base, mixins.IdentityMixin):
    __tablename__ = 'repository'
    __mapper_args__ = {
        'polymorphic_identity': 'Repository',
    }

    host_name = Column(
        'host_name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=False,
    )

    share_name = Column(
        'share_name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=False,
    )

    def __init__(self, **kwargs):
        super(Repository, self).__init__()
        self._setKeywordFields(**kwargs)
        return


class Path(base.Base, mixins.IdentityMixin):
    __tablename__ = 'path'
    __mapper_args__ = {
        'polymorphic_identity': 'Path',
    }

    parent_id = Column(
        'parent_id',
        Integer,
        ForeignKey('path.id'),
        nullable=True,
    )

    children = relationship(
        'Path',

        # TODO: Try to get the 'parent' relationship working.
        # # many to one + adjacency list - remote_side
        # # is required to reference the 'remote'
        # # column in the join condition.
        # backref=backref(
        #     'parent',
        #     remote_side='Path.id',
        #     single_parent=True,
        #     cascade='save-update, merge, delete, delete-orphan'
        # ),

        # children will be represented as a dictionary
        # on the "name" attribute.
        collection_class=attribute_mapped_collection('path'),
    )

    repository_id = Column(
        'repository_id',
        Integer,
        ForeignKey('repository.id'),
        nullable=True,
        unique=False,
    )

    repository = relationship(
        'Repository',
        foreign_keys=[repository_id]
    )

    # TODO: Separate this field into a 'repo' field as well as path, this means
    # we can change the sever and share that the file exist on by just updating
    # one (repo) field.
    path = Column(
        'path',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=False,  # TODO: Turn this back on and make sure tests don't fail this.
    )

    is_file = Column(
        'is_file',
        Boolean,
        nullable=False,
        unique=False,
    )

    mime_id = Column(
        'mime_id',
        Integer,
        ForeignKey('mime.id'),
        nullable=True,
        unique=False,
    )

    mime = relationship(
        'Mime',
        foreign_keys=[mime_id]
    )

    file_size = Column(
        'file_size',
        BigInteger,
        nullable=True,
        unique=False,
    )

    path_tags = relationship(
        'PathTag',
    )

    def __init__(self, **kwargs):
        super(Path, self).__init__()
        # Sanitise the path into ASCII characters.
        kwargs['path'] = kwargs['path'].encode('ascii', errors='ignore')
        self._setKeywordFields(**kwargs)
        return


class PathTag(base.Base):
    __tablename__ = 'path_tag'
    __mapper_args__ = {
        'polymorphic_identity': 'PathTag',
    }

    tag_id = Column(
        'tag_id',
        Integer,
        ForeignKey('tag.id'),
        primary_key=True,
        autoincrement=True,
    )

    path_id = Column(
        'path_id',
        Integer,
        ForeignKey('path.id'),
        primary_key=True,
    )

    tag = relationship('Tag')

    path = relationship('Path')

    def __init__(self, tag, path):
        super(PathTag, self).__init__()
        self.tag = tag
        self.path = path


class Tag(base.Base, mixins.IdentityMixin):
    __tablename__ = 'tag'
    __mapper_args__ = {
        'polymorphic_identity': 'Tag',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(Tag, self).__init__()
        self._setKeywordFields(**kwargs)


class Mime(base.Base, mixins.IdentityMixin):
    __tablename__ = 'mime'
    __mapper_args__ = {
        'polymorphic_identity': 'Mime',
    }

    mime_type_id = Column(
        'mime_type_id',
        Integer,
        ForeignKey('mime_type.id'),
        nullable=True,
        unique=False,
    )

    mime_subtype_id = Column(
        'mime_subtype_id',
        Integer,
        ForeignKey('mime_subtype.id'),
        nullable=True,
        unique=False,
    )

    mime_type = relationship('MimeType')

    mime_subtype = relationship('MimeSubtype')

    def __init__(self, **kwargs):
        super(Mime, self).__init__()
        self._setKeywordFields(**kwargs)


class MimeType(base.Base, mixins.IdentityMixin):
    __tablename__ = 'mime_type'
    __mapper_args__ = {
        'polymorphic_identity': 'MimeType',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(MimeType, self).__init__()
        self._setKeywordFields(**kwargs)


class MimeSubtype(base.Base, mixins.IdentityMixin):
    __tablename__ = 'mime_subtype'
    __mapper_args__ = {
        'polymorphic_identity': 'MimeSubtype',
    }

    name = Column(
        'name',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        super(MimeSubtype, self).__init__()
        self._setKeywordFields(**kwargs)
