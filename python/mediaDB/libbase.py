
import os
import os.path
import json
import collections
import functools
import traceback

import MySQLdb
import MySQLdb.cursors


class Media(object):
    def __init__(self, values, tags=None):
        super(Media, self).__init__()
        self.id = None
        self.path = None
        self.dirname = None
        self.name = None
        self.extension = None
        self.media_type = None
        self.mime_type = None
        self.size = None
        self.tags = []
        if len(values) == 0:
            return

        self.id = values[0]
        self.path = values[1]
        self.dirname = values[2]
        self.name = values[3]
        self.extension = values[4]
        self.mime_type = values[5]
        self.size = values[6]
        if tags:
            self.tags = tags
        return


class memoized(object):
    """
    Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).

    From:
    https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


@memoized
def __readData(filePath):
    """
    Read file path as JSON data format.

    :param filePath: File path to .json file. 
    :return: Contents of the .json file.
    """
    f = open(filePath, 'rb')
    data = json.load(f)
    f.close()
    return data


def getSystemConfigPath():
    baseDir = os.path.dirname(__file__)
    name = 'mediaDB_linux.json'
    if os.name == 'nt':
        name = 'mediaDB_windows.json'
    path = os.path.join(baseDir, '..', '..', 'config', name)
    path = os.path.abspath(path)
    return path


def getWordConfigPath():
    baseDir = os.path.dirname(__file__)
    name = 'mediaDB_words.json'
    path = os.path.join(baseDir, '..', '..', 'config', name)
    path = os.path.abspath(path)
    return path


def getMimeFilePaths():
    baseDir = os.path.dirname(__file__)
    path = os.path.join(baseDir, '..', '..', 'data', 'mime')
    path = os.path.abspath(path)
    names = os.listdir(path)
    paths = []
    for p in names:
        p = os.path.join(path, p)
        paths.append(p)
    return paths


def readConfig(path=None):
    if path is None:
        path = getSystemConfigPath()
    assert os.path.isfile(path)
    data = __readData(path)
    return data


def getHostName():
    key = 'hostname'
    path = getSystemConfigPath()
    data = readConfig(path)
    assert key in data
    return data[key]


def getUserName():
    key = 'username'
    path = getSystemConfigPath()
    data = readConfig(path)
    assert key in data
    return data[key]


def getPassword():
    key = 'password'
    path = getSystemConfigPath()
    data = readConfig(path)
    assert key in data
    return data[key]


def getDBName():
    key = 'database'
    path = getSystemConfigPath()
    data = readConfig(path)
    assert key in data
    return data[key]


def getPort():
    key = 'port'
    path = getSystemConfigPath()
    data = readConfig(path)
    assert key in data
    return data[key]


def getIncludePaths():
    key = 'includes'
    path = getSystemConfigPath()
    data = readConfig(path)
    assert key in data
    return data[key]


def getExcludePaths():
    key = 'excludes'
    path = getSystemConfigPath()
    data = readConfig(path)
    assert key in data
    return data[key]


def getSplitChars():
    key = 'split_chars'
    path = getWordConfigPath()
    data = readConfig(path)
    assert key in data
    return data[key]


def getExcludedWords():
    key = 'excluded_words'
    path = getWordConfigPath()
    data = readConfig(path)
    assert key in data
    return data[key]


def connectToDatabase(host=None,
                      user=None, password=None,
                      name=None, port=None,
                      verbose=True):
    if host is None:
        host = getHostName()
    if user is None:
        user = getUserName()
    if password is None:
        password = getPassword()
    if name is None:
        name = getDBName()
    if port is None:
        port = getPort()

    if verbose:
        print 'Connecting...'
        print 'Host:', host
        print 'User:', user
        print 'Password:', password
        print 'DB Name:', name
        print 'Port:', port

    db = MySQLdb.connect(
        host=host,
        user=user,
        passwd=password,
        db=name,
        port=port,
        charset='utf8',
        use_unicode=True
    )
    return db


def commitWrite(db, cursor, sql, *args, **kwargs):
    # Prepare SQL query to INSERT a record into the database.
    ok = None
    try:
        # Execute the SQL command
        cursor.execute(sql, *args)

        # Commit your changes in the database
        db.commit()
        ok = True
    except:
        # Rollback in case there is any error
        db.rollback()
        ok = False
        print 'ERROR: SQL:', repr(sql)
        print 'ERROR: Args:'
        for i, arg in enumerate(args):
            print '>', i, repr(arg)
        # trace = traceback.format_exc()
        # print trace
        raise

    return ok


def commitReadOne(db, cursor, sql, *args):
    cursor.execute(sql,*args)
    return cursor.fetchone()


def commitReadAll(db, cursor, sql, *args):
    cursor.execute(sql, *args)
    return cursor.fetchall()


def getServerVersion(db, cursor, verbose=True):
    data = commitReadOne(db, cursor, 'SELECT VERSION()')
    print 'Database Version:', data[0]
    return data[0]

