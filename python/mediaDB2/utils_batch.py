from sqlalchemy import *

import mimetypes
import uuid


def createRepoKeywords(mount):
    hostname = mount['hostname']
    share = mount['share']
    if isinstance(hostname, basestring) and len(hostname) == 0:
        return None
    if isinstance(share, basestring) and len(share) == 0:
        return None
    return {
        'host_name': hostname,
        'share_name': share,
        'code': uuid.uuid4()
    }


def createMimeKeywords(path):
    mime_type_kw = {}
    mime_subtype_kw = {}

    mime = mimetypes.guess_type(path, strict=False)
    if mime and len(mime) == 2 and mime[0]:
        tmp = str(mime[0]).split('/')
        type_name = tmp[0]
        subtype_name = tmp[1]

        mime_type_kw['name'] = type_name
        mime_type_kw['code'] = uuid.uuid4()

        mime_subtype_kw['name'] = subtype_name
        mime_subtype_kw['code'] = uuid.uuid4()
    else:
        mime_type_kw = None
        mime_subtype_kw = None

    return mime_type_kw, mime_subtype_kw


def generateSqlInsertIfExists(Model, column_names, unique_names):
    """
    Create SQL code to insert a row if the row doesn't already exist.

    Uses SQLAlchemy Core to generate the SQL code.

    Generates:
    INSERT INTO table_name (column_name1, column_name2, code)
    SELECT %(bind_name1)s, %(bind_name2)s, 'new_random_uuid'
    WHERE NOT (
        EXISTS (
            SELECT table_name.id
            FROM table_name
            WHERE table_name.column_name1 = %(bind_name1)s AND
                  table_name.column_name2 = %(bind_name2)s
        )
    )
    LIMIT 1

    :param Model: The SQLAlchemy ORM model for the inserted row.
    :param column_names:
    :param unique_names:
    :return:
    """
    tbl = Model.__table__

    binds = []
    cols = []
    for col in tbl.c:
        if col.name in column_names:
            cols.append(col)
            binds.append(bindparam(col.name))

    unique_ops = []
    for col, bp in zip(cols, binds):
        if col.name in unique_names:
            unique_ops.append(col == bp)

    sel = select(binds)
    whr = sel.where(~exists([tbl.c.id]).where(and_(*unique_ops)))
    # whr = whr.limit(literal(1))
    ins = insert(Model).from_select(cols, whr)

    # tbl = Repository.__table__
    # cols = [tbl.c.host_name, tbl.c.share_name, tbl.c.code]
    # values = [bindparam('host_name'), bindparam('share_name'), bindparam('code')]
    # # values = [literal(kw['host_name']), literal(kw['share_name']), literal(uuid.uuid4())]
    # sel = select(values)
    # whr = sel.where(~exists([tbl.c.id]).where(and_(tbl.c.host_name == bindparam('host_name'),
    #                                                tbl.c.share_name == bindparam('share_name'))))
    # whr = whr.limit(literal(1))
    # ins = insert(tbl).from_select(cols, whr)

    return ins


def generateSqlSelectId(Model, column_names):
    """
    Create SQL code to select ids of matching column values.

    Uses SQLAlchemy Core to generate the SQL code.

    Generates:
    SELECT table_name.id
    FROM table_name
    WHERE table_name.column_name1 == %(bind_name1)s AND
          table_name.column_name2 == %(bind_name2)s

    :param Model:
    :param column_names:
    :return:
    """
    tbl = Model.__table__

    cols = []
    values = []
    for col in tbl.c:
        if col.name in column_names:
            values.append(bindparam(col.name))
            cols.append(col)

    conds = []
    for col, bp in zip(cols, values):
        conds.append(col == bp)

    return select([tbl.c.id]).where(and_(*conds))

# def addPaths(session, full_paths):
#     """
#     This function was an attempt to speed up adding data to the database.
#
#     :param session:
#     :param full_paths:
#     :return:
#     """
#     # Repository
#     end_paths = []
#     params = []
#     added = {}
#     for full_path in full_paths:
#         mount_dir, mount = mediaDB2.mounts.getMount(mediaDB2.mounts.MOUNTS, full_path)
#
#         # Get the final end_path
#         end_path = full_path[len(mount_dir):]
#         end_path = end_path.encode('ascii', errors='ignore')
#         end_path_len = len(end_path.strip())
#         if end_path_len == 0:
#             return 0
#         elif end_path_len > 255:
#             msg = 'Warning: File path exceeds allowed character length, %r.'
#             print msg % full_path
#             return 0
#         end_paths.append(end_path)
#
#         #
#         kw = None
#         if mount:
#             kw = createRepoKeywords(mount)
#         if kw is None:
#             msg = 'Warning: Could not create repository for file path, %r.'
#             print msg % full_path
#             return 0
#         kw_str = str(kw)
#         if kw_str not in added:
#             added[kw_str] = True
#             params.append(kw)
#
#     # Create Repository
#     sql = generateSqlInsertIfExists(
#         Repository,
#         ['host_name', 'share_name', 'code'],
#         ['host_name', 'share_name']
#     )
#     session.execute(sql, params)
#
#     # # Query Repository
#     # sql = generateSqlSelectId(Repository, ['host_name', 'share_name'])
#     # r = session.execute(sql, params)
#     # rows = r.fetchall()
#     # # print 'rows:', rows
#
#     # File path metadata query
#     is_files = []
#     sizes = []
#     tags = []
#     for full_path, end_path in zip(full_paths, end_paths):
#         is_file = None
#         size = None
#         if os.path.isdir(full_path):
#             is_file = False
#         elif os.path.isfile(full_path):
#             is_file = True
#
#             size = 0
#             try:
#                 size = os.path.getsize(full_path)
#             except OSError:
#                 pass
#
#         tagNames = createTagNames(end_path)
#         for name in tagNames:
#             tags.append({
#                 'name': name,
#                 'code': uuid.uuid4()
#             })
#
#         sizes.append(size)
#         is_files.append(is_file)
#
#     # Create MimeType
#     if len(tags) > 0:
#         sql = generateSqlInsertIfExists(
#             Tag,
#             ['name', 'code'],
#             ['name']
#         )
#         session.execute(sql, tags)
#
#     # Get Mime* Parameters
#     type_params = []
#     subtype_params = []
#     for full_path in full_paths:
#         mime_type_kw, mime_subtype_kw = createMimeKeywords(full_path)
#         if mime_type_kw is not None:
#             type_params.append(mime_type_kw)
#         if mime_subtype_kw is not None:
#             subtype_params.append(mime_subtype_kw)
#
#     # Create MimeType
#     if len(type_params) > 0:
#         sql = generateSqlInsertIfExists(
#             MimeType,
#             ['name', 'code'],
#             ['name']
#         )
#         session.execute(sql, type_params)
#
#     # Create MimeSubtype
#     if len(subtype_params) > 0:
#         sql = generateSqlInsertIfExists(
#             MimeSubtype,
#             ['name', 'code'],
#             ['name']
#         )
#         session.execute(sql, subtype_params)
#
#     # Path
#     params = []
#     for full_path, end_path, size, is_file in zip(full_paths, end_paths, sizes, is_files):
#         kw = {}
#
#         kw['path'] = end_path
#         kw['code'] = uuid.uuid4()
#
#         extension = None
#         if is_file is False:
#             kw['is_file'] = False
#             kw['file_size'] = None
#             kw['mime_id'] = None
#
#         elif is_file is True:
#             kw['is_file'] = True
#             kw['file_size'] = size
#             kw['mime_id'] = None
#
#             # # MIME type
#             # mime = createMime(session, full_path)
#
#         else:
#             msg = 'Warning: File path is invalid, %r.'
#             print msg % full_path
#             continue
#
#         kw['repository_id'] = None  # TODO: Get the repo id from the database.
#         kw['parent_id'] = None  # TODO: Get the parent id from the database.
#
#         params.append(kw)
#
#     #
#     sql = generateSqlInsertIfExists(
#         Path,
#         ['path', 'is_file', 'file_size', 'mime_id', 'parent_id', 'repository_id', 'code'],
#         ['path', 'is_file']
#     )
#     session.execute(sql, params)
#
#     # #
#     # sql = generateSqlSelect(Path, ['path'])
#     # r = session.execute(sql, params)
#     # # rows = r.fetchall()
#     # # print 'rows:', rows
#
#     return len(full_paths)