"""
Test script for assetDB.

Traceback (most recent call last):
  File "test.py", line 199, in <module>
    main()
  File "test.py", line 182, in main
    num = findMedia(session, path, excludes=excludes)
  File "test.py", line 158, in findMedia
    session.commit()
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/orm/session.py", line 921, in commit
    self.transaction.commit()
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/orm/session.py", line 461, in commit
    self._prepare_impl()
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/orm/session.py", line 441, in _prepare_impl
    self.session.flush()
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/orm/session.py", line 2213, in flush
    self._flush(objects)
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/orm/session.py", line 2333, in _flush
    transaction.rollback(_capture_exception=True)
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/util/langhelpers.py", line 66, in __exit__
    compat.reraise(exc_type, exc_value, exc_tb)
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/orm/session.py", line 2297, in _flush
    flush_context.execute()
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/orm/unitofwork.py", line 389, in execute
    rec.execute(self)
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/orm/unitofwork.py", line 554, in execute
    uow
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/orm/persistence.py", line 181, in save_obj
    mapper, table, insert)
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/orm/persistence.py", line 860, in _emit_insert_statements
    execute(statement, params)
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 945, in execute
    return meth(self, multiparams, params)
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/sql/elements.py", line 269, in _execute_on_connection
    return connection._execute_clauseelement(self, multiparams, params)
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1053, in _execute_clauseelement
    compiled_sql, distilled_params
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1189, in _execute_context
    context)
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1402, in _handle_dbapi_exception
    exc_info
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/util/compat.py", line 203, in raise_from_cause
    reraise(type(exception), exception, tb=exc_tb, cause=cause)
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1182, in _execute_context
    context)
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/engine/default.py", line 504, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.IntegrityError: (psycopg2.IntegrityError) duplicate key value violates unique constraint "mime_subtype_name_key"
DETAIL:  Key (name)=(vnd.lotus-screencam) already exists.
 [SQL: 'INSERT INTO mime_subtype (code, name) VALUES (%(code)s, %(name)s) RETURNING mime_subtype.id'] [parameters: {'code': UUID('79cd3175-e203-4f41-b626-4e9c831377aa'), 'name': 'vnd.lotus-screencam'}]

"""
import mimetypes
import os
import os.path
import sys
import time
import pprint

from sqlalchemy import create_engine

import mediaDB2.config as config
import mediaDB2.setup as setup
import mediaDB2.models.modelbase as base
import mediaDB2.models.path
from mediaDB2.models import *

# initialise mimetypes with user-defined values.
mime_files = config.getMimeFilePaths()
mimetypes.init(mime_files)

SPLIT_CHARS = config.getSplitChars()
UNNEEDED_WORDS = config.getExcludedWords()
MOUNTS = mediaDB2.models.path.getAllMounts()


def loopFiles(session, files, dirpath, exclude, parent_dir):
    paths = []
    for filename in files:
        if filename.startswith('.'):
            continue
        if filename.startswith('@'):
            continue
        if filename.endswith('#'):
            continue
        if filename.endswith('~'):
            continue

        full_path = os.path.abspath(os.path.join(dirpath, filename))
        if not os.path.isfile(full_path):
            continue

        if exclude is not None:
            ok = True
            for ex in exclude:
                if full_path.startswith(ex):
                    ok = False
                    break
            if ok is False:
                continue

        # Size
        try:
            size = os.path.getsize(full_path)
        except:
            size = 0

        # MIME type
        mime = mediaDB2.models.path.createMime(session, full_path)
        session.commit()

        # Repository
        mount = mediaDB2.models.path.getMount(MOUNTS, full_path)
        repository = None
        if mount:
            repository = mediaDB2.models.path.createRepo(session, mount)
        session.commit()

        # Path
        p = Path(path=full_path, is_file=True, file_size=size)
        p.mime = mime
        p.repository = repository
        p.parent = parent_dir
        paths.append(p)

        # File Extension
        n, ext = os.path.splitext(full_path)
        extension = ext[1:].lower()

        # Tags
        path = full_path[len(dirpath):]  # Only use file name for tags.
        tag_names = mediaDB2.models.path.createTags(path, extension)
        for name in tag_names:
            tag = session.query(Tag).filter_by(name=name).first()
            if tag is None:
                tag = Tag(name=name)
                session.add(tag)
            pt = PathTag(tag=tag, path=p)
            p.path_tags.append(pt)

        session.commit()

    return paths


def printDots(c):
    if c > 100:
        n = c / 100
        for i in range(n):
            sys.stdout.write('.')
            sys.stdout.flush()
        c = c % 100
    return c


def findMedia(session, root_path, excludes=None):
    c = 0
    num = 0
    root_dir_objs = {}
    for root, dirs, files in os.walk(root_path, topdown=True, followlinks=False):
        # TODO: Get proper 'repo' path. Something like "\\HEARTOFGOLD\Music".

        # Repository
        mount = mediaDB2.models.path.getMount(MOUNTS, root)
        repository = None
        if mount:
            repository = mediaDB2.models.path.createRepo(session, mount)
        session.add_all([repository])

        d = None
        if root not in root_dir_objs:
            d = Path(path=root, is_file=False)
            root_dir_objs[root] = d
            session.add(d)
            num += 1
            c += 1
        else:
            d = root_dir_objs[root]

        paths = loopFiles(session, files, root, excludes, d)
        num_paths = len(paths)
        num += num_paths
        c += num_paths

        session.add_all(paths)
        session.commit()

        c = printDots(c)

        for dirname in dirs:
            if dirname.startswith('.'):
                continue
            if dirname.startswith('@'):
                continue
            if dirname.endswith('#'):
                continue
            if dirname.endswith('~'):
                continue

            files = []
            dirpath = os.path.abspath(os.path.join(root, dirname))
            if os.path.isdir(dirpath):
                d = Path(path=dirpath, is_file=False)
                session.add(d)
                num += 1
                c += 1

                try:
                    files = os.listdir(dirpath)
                except:
                    continue

                paths = loopFiles(session, files, dirpath, excludes, d)
                num_paths = len(paths)
                num += num_paths
                c += num_paths
                session.add_all(paths)
                session.commit()

                c = printDots(c)

    return num


def main():
    # print 'args', sys.argv
    reset_tables = False
    if len(sys.argv) > 1:
        reset_tables = bool(str(sys.argv[1]))
    print 'reset_tables:', reset_tables

    url = setup.get_database_url()
    engine = create_engine(url, echo=setup.ECHO)

    # Reset Tables
    if reset_tables is True:
        base.dropTables(engine)
        base.createTables(engine)

    session = setup.get_session(autoflush=False)

    # Find Media
    includes = config.getIncludePaths()
    excludes = config.getExcludePaths()
    for path in includes:
        print 'Find Media...', path
        s = time.time()

        num = findMedia(session, path, excludes=excludes)

        e = time.time()
        total = e - s
        per_total = 0.0
        if num > 0:
            per_total = (total / num)

        print ''
        print 'Path =', path
        print 'Count =', str(num)
        print 'Per-Insert Time = %.4g seconds' % per_total
        print 'Total Time = %.4g seconds' % total
        print 'Finished.'


if __name__ == '__main__':
    main()
