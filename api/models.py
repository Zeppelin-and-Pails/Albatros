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
from sqlalchemy.pool import NullPool
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

DIR = os.path.dirname(os.path.realpath(__file__))
conf = yaml.safe_load(open("{}/db.cfg".format(DIR)))

def get_table(table):
    """
    Get the named table from the database, automatically loading it into a model
    :param table:   the name of the requested table, case sensetive if the database is
    :return:    an sqlalchemy.Table object
    """
    engine = db_connect()
    meta = MetaData(bind=engine)
    return Table(table, meta, autoload=True, autoload_with=engine)

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    :return:    an sqlalchemy.engine object
    """
    database = {
        'drivername': 'postgresql+pg8000',
        'host':       conf['host'],
        'port':       conf['port'],
        'username':   conf['user'],
        'password':   conf['pass'],
        'database':   conf['database'],
    }
    return create_engine(URL(**database), poolclass=NullPool)

def get_addresses_statement():
    ad   = get_table('address_detail')
    amb2 = get_table('address_mesh_block_2011')
    m2   = get_table('mb_2011')
    site = get_table('address_site')
    l    = get_table('locality')
    sl   = get_table('street_locality')
    s    = get_table('state')
    lp   = get_table('locality_point')
    adg  = get_table('address_default_geocode')
    slp  = get_table('street_locality_point')

    Session = sessionmaker(bind=db_connect())
    session = Session()
    result  = session.query(
        ad.c.address_detail_pid
        , ad.c.building_name
        , ad.c.lot_number_prefix
        , ad.c.lot_number
        , ad.c.lot_number_suffix
        , ad.c.flat_type_code
        , ad.c.flat_number_prefix
        , ad.c.flat_number
        , ad.c.flat_number_suffix
        , ad.c.level_type_code
        , ad.c.level_number_prefix
        , ad.c.level_number
        , ad.c.level_number_suffix
        , ad.c.number_first_prefix
        , ad.c.number_first
        , ad.c.number_first_suffix
        , ad.c.number_last_prefix
        , ad.c.number_last
        , ad.c.number_last_suffix
        , ad.c.location_description
        , ad.c.alias_principal
        , ad.c.postcode
        , ad.c.private_street
        , ad.c.legal_parcel_id
        , ad.c.confidence
        , ad.c.level_geocoded_code
        , ad.c.property_pid
        , ad.c.gnaf_property_pid
        , ad.c.primary_secondary
        , m2.c.mb_2011_code
        , amb2.c.mb_match_code
        , sl.c.street_class_code
        , sl.c.street_name
        , sl.c.street_type_code
        , sl.c.street_suffix_code
        , sl.c.gnaf_street_pid
        , sl.c.gnaf_street_confidence
        , sl.c.gnaf_reliability_code.label('street_gnaf_reliability_code')
        , l.c.locality_name
        , l.c.primary_postcode
        , l.c.locality_class_code
        , l.c.gnaf_locality_pid
        , l.c.gnaf_reliability_code.label('locality_gnaf_reliability_code')
        , s.c.state_abbreviation
        , lp.c.planimetric_accuracy.label('locality_planimetric_accuracy')
        , lp.c.longitude.label('locality_longitude')
        , lp.c.latitude.label('locality_latitude')
        , site.c.address_type
        , site.c.address_site_name
        , adg.c.geocode_type_code
        , adg.c.longitude.label('longitude')
        , adg.c.latitude.label('latitude')
        , slp.c.boundary_extent.label('boundary_extent')
        , slp.c.planimetric_accuracy.label('street_planimetric_accuracy')
        , slp.c.longitude.label('street_longitude')
        , slp.c.latitude.label('street_latitude')
    ).\
        outerjoin(amb2, amb2.c.address_detail_pid == ad.c.address_detail_pid).\
        outerjoin(m2, m2.c.mb_2011_pid == amb2.c.mb_2011_pid).\
        outerjoin(site, site.c.address_site_pid == ad.c.address_site_pid).\
        outerjoin(l, l.c.locality_pid == ad.c.locality_pid).\
        outerjoin(sl, sl.c.street_locality_pid == ad.c.street_locality_pid).\
        outerjoin(s, s.c.state_pid == l.c.state_pid).\
        outerjoin(lp, lp.c.locality_pid == l.c.locality_pid).\
        outerjoin(adg, adg.c.address_detail_pid == ad.c.address_detail_pid).\
        outerjoin(slp, slp.c.street_locality_pid == sl.c.street_locality_pid)

    return "CREATE OR REPLACE VIEW addresses AS {}".format(result.statement)
