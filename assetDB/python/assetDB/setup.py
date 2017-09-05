"""

"""

import os
import sys
import random
import getpass

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
# from sqlalchemy.orm import create_session
from sqlalchemy.orm import sessionmaker

import assetDB.config as config

# Default database type
# 'mysql' or 'postgres'
DB_TYPE = 'mysql'
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


SITES = []


def set_sites(session, sites):
    global SITES
    session.add_all(sites)
    session.commit()
    SITES = sites
    return


def get_sites(session):
    q = session.query('site')
    sites = q.all()
    return sites


def get_current_site():
    global SITES
    site_id = None
    # assert len(SITES) > 0
    if len(SITES) > 0:
        site = random.choice(SITES)
        site_id = site.id
    return site_id


USERS = []


# def set_users(session, users):
#     global USERS
#     session.add_all(users)
#     session.commit()
#     USERS = users
#     return
#
#
# def get_users(session):
#     q = session.query('site')
#     users = q.all()
#     return users


def get_current_user():
    user_name = getpass.getuser()
    try:
        session = get_session()
        q = session.query('user').filter_by(name=user_name)
        users = q.all()
    except Exception:
        users = []

    userId = None
    if len(users) > 0:
        user = random.choice(users)
        userId = user.id
    return userId

