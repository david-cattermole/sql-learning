"""
File Data database tables
"""

import os
import subprocess
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

SPLIT_CHARS = config.getSplitChars()
UNNEEDED_WORDS = config.getExcludedWords()


def getAllMounts():
    mounts = {}
    if os.name == 'nt':
        return mounts
    lines = subprocess.check_output(['mount', '-l']).split('\n')
    for line in lines:
        parts = line.split(' ')
        if len(parts) > 2:
            repo = parts[0]
            directory = parts[2]
            typ = parts[4]

            hostname = ''
            share = ''
            if ':' in repo:
                splt = repo.split(':')
                hostname = splt[0]
                share = splt[1]

            mounts[directory] = {
                'repo': repo,
                'hostname': hostname,
                'share': share,
                'type': typ,
            }
    return mounts


def getMount(mounts, path):
    mount = None
    for d in mounts.keys():
        if path.startswith(d) is True:
            mount = mounts[d]
            break
    return mount


def createRepo(session, mount):
    hostname = mount['hostname']
    share = mount['share']

    q = session.query(Repository)
    q = q.filter(Repository.host_name == hostname, Repository.share_name == share)
    repo = q.first()

    if repo is None:
        repo = Repository(host_name=hostname, share_name=share)
        session.add(repo)
    return repo


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
    mime_obj = None

    mime = mimetypes.guess_type(path, strict=False)
    if mime and len(mime) == 2 and mime[0]:
        tmp = str(mime[0]).split('/')
        type_name = tmp[0]
        subtype_name = tmp[1]

        # Query Mime
        q_mime = session.query(Mime).join(MimeType, MimeSubtype)
        q_mime = q_mime.filter(MimeType.name == type_name,
                               MimeSubtype.name == subtype_name)
        mime_obj = q_mime.first()
        if mime_obj is None:
            # Mime Type
            q_type = session.query(MimeType)
            q_type = q_type.filter(MimeType.name == type_name)
            mime_type = q_type.first()
            if mime_type is None:
                mime_type = MimeType(name=type_name)
                session.add(mime_type)

            # Mime Sub-type
            q_subtype = session.query(MimeSubtype)
            q_subtype = q_subtype.filter(MimeSubtype.name == subtype_name)
            mime_subtype = q_subtype.first()
            if mime_subtype is None:
                mime_subtype = MimeSubtype(name=subtype_name)
                session.add(mime_subtype)

            # Mime Object
            mime_obj = Mime(
                mime_type=mime_type,
                mime_subtype=mime_subtype
            )
            session.add(mime_obj)

    return mime_obj


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
