"""

"""

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

import mediaDB2.config as config

# Default database type
# 'mysql' or 'postgres'
DB_TYPE = 'postgres'
ECHO = False


def get_database_url(dbtype=None):
    if dbtype is None:
        dbtype = DB_TYPE
    dbconfig = config.getDbConfig(dbtype)
    url = URL(**dbconfig)
    return url


def get_session(dbtype=None, echo=None):
    if dbtype is None:
        dbtype = DB_TYPE
    if echo is None:
        echo = ECHO
    url = get_database_url(dbtype)
    print 'URL:', url
    engine = create_engine(url, echo=echo)
    Session = sessionmaker(bind=engine)
    return Session()

