"""
Functions to read config files.
"""

import os
import os.path
import json
import collections
import functools
import traceback

from mediaDB2.cache import memoized


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


def getPathFromProjectRoot(*args):
    baseDir = os.path.dirname(__file__)
    path = os.path.join(baseDir, '..', '..', *args)
    path = os.path.abspath(path)
    return path


def getSystemConfigPath():
    name = 'mediaDB2_linux.json'
    if os.name == 'nt':
        name = 'mediaDB2_windows.json'
    return getPathFromProjectRoot('config', name)


def getDbConfigPath(name):
    assert isinstance(name, str)
    name = 'mediaDB2_' + name + '.json'
    return getPathFromProjectRoot('config', 'db', name)


def getLayoutConfigPath(name):
    assert isinstance(name, str)
    name = 'mediaDB2_' + name + '.json'
    return getPathFromProjectRoot('config', name)


def getSiteConfigPath(name):
    assert isinstance(name, str)
    name = 'mediaDB2_' + name + '.json'
    return getPathFromProjectRoot('config', 'site', name)


def getDbConfig(name):
    path = getDbConfigPath(name)
    return __readData(path)


def getLayoutConfig(name):
    path = getDbConfigPath(name)
    return __readData(path)


def getSiteConfig(name):
    path = getSiteConfigPath(name)
    return __readData(path)


def readSystemConfig(path=None):
    if path is None:
        path = getSystemConfigPath()
    assert os.path.isfile(path)
    data = __readData(path)
    return data


def getWordConfigPath():
    name = 'mediaDB2_words.json'
    path = getPathFromProjectRoot('config', name)
    return path


def getMimeFilePaths():
    path = getPathFromProjectRoot('data', 'mime')
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
