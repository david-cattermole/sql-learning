"""
File Data database tables
"""

import mimetypes
import re

from sqlalchemy import (
    Column, Integer, BigInteger, String, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

import mediaDB2.config as config
from mediaDB2.models import mixins
from mediaDB2.models import modelbase as base

# initialise mimetypes with user-defined values.
files = config.getMimeFilePaths()
mimetypes.init(files)

MIME_TYPE_OBJS = {}
MIME_SUBTYPE_OBJS = {}

SPLIT_CHARS = config.getSplitChars()
UNNEEDED_WORDS = config.getExcludedWords()


def createTags(path, file_ext):
    split = path.strip()

    for char in SPLIT_CHARS:
        split = split.replace(char, ' ').strip()
    tags = []
    tmp = re.split(r'([A-Z]+[a-z]*)', split)
    for tag in tmp:
        tag = tag.strip()
        if len(tag):
            if tag not in tags:
                tags.append(tag)
            dashSplit = tag.split('-')
            if len(dashSplit) > 1:
                for t in dashSplit:
                    if t not in tags:
                        tags.append(t)
    the_tags = []
    for tag in tags:
        tag = tag.lower()
        if len(tag) <= 1:
            continue
        if not tag.isalpha():
            continue
        if tag in UNNEEDED_WORDS:
            continue
        if tag == file_ext:
            continue
        if tag not in the_tags:
            the_tags.append(tag)
    return the_tags


def createMime(session, path):
    global MIME_TYPE_OBJS
    global MIME_SUBTYPE_OBJS

    mime_type = None
    mime_subtype = None

    mime = mimetypes.guess_type(path, strict=False)
    if mime and len(mime) == 2 and mime[0]:
        tmp = str(mime[0]).split('/')
        type_name = tmp[0]
        subtype_name = tmp[1]

        if type_name not in MIME_TYPE_OBJS:
            q_type = session.query(MimeType).filter(MimeType.name == type_name)
            mime_type = q_type.first()
            if mime_type is not None:
                MIME_TYPE_OBJS[type_name] = mime_type
        else:
            mime_type = MIME_TYPE_OBJS[type_name]
        if mime_type is None:
            mime_type = MimeType(name=type_name)

        if subtype_name not in MIME_SUBTYPE_OBJS:
            q_subtype = session.query(MimeSubtype).filter(MimeSubtype.name == subtype_name)
            mime_subtype = q_subtype.first()
            if mime_subtype is not None:
                MIME_SUBTYPE_OBJS[subtype_name] = mime_subtype
        else:
            mime_subtype = MIME_SUBTYPE_OBJS[subtype_name]
        if mime_subtype is None:
            mime_subtype = MimeSubtype(name=subtype_name)

    return mime_type, mime_subtype


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

    # TODO: Separate this field into a 'repo' field as well as path, this means
    # we can change the sever and share that the file exist on by just updating
    # one (repo) field.
    path = Column(
        'path',
        String(base.NAME_LENGTH),
        nullable=False,
        unique=False,  # TOOD: Turn this back on and make sure tests don't fail this.
    )

    is_file = Column(
        'is_file',
        Boolean,
        nullable=False,
        unique=False,
    )

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

    file_size = Column(
        'file_size',
        BigInteger,
        nullable=True,
        unique=False,
    )

    path_tags = relationship(
        'PathTag',
    )

    mime_type = relationship('MimeType')

    mime_subtype = relationship('MimeSubtype')

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
