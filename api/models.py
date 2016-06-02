# -*- coding: utf-8 -*-
"""
Albatros Database Models

Database Models for Albatros

@category   Utility
@version    $ID: 1.1.1, 2016-05-05 17:00:00 CST $;
@author     KMR
@licence    GNU GPL v.3
"""
import os, yaml
from sqlalchemy import *
from sqlalchemy.engine.url import URL

DIR = os.path.dirname(os.path.realpath(__file__))
conf = yaml.safe_load(open("{}/db.cfg".format(DIR)))

def get_table(table):
    """
    Get the named table from the database, automaticall loading it into a model
    :param table:
    the name of the requested table, case sensetive if the database is
    :return:
    an sqlalchemy.Table object
    """
    engine = db_connect()
    meta = MetaData(bind=engine)
    return Table(table, meta, autoload=True, autoload_with=engine)

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    :return:
    an sqlalchemy.engine object
    """
    database = {
        'drivername': 'postgresql+pg8000',
        'host':       conf['host'],
        'port':       conf['port'],
        'username':   conf['user'],
        'password':   conf['pass'],
        'database':   conf['database']
    }
    return create_engine(URL(**database))
