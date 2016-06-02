#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Albatros API

Data importer for Albatros

@category   Utility
@version    $ID: 1.1.1, 2016-05-05 17:00:00 CST $;
@author     KMR
@licence    GNU GPL v.3
"""
import os
import glob
import yaml
import zipfile
import urllib2
from api import models
from sqlalchemy import text

DIR = os.path.dirname(os.path.realpath(__file__))
conf = yaml.safe_load(open("{}/data_importer.cfg".format(DIR)))

type_map = {
    'default'                : 'text',
    'date_created'           : 'date',
    'date_retired'           : 'date',
    'date_last_modified'     : 'date',
    'flat_number'            : 'int',
    'level_number'           : 'int',
    'number_first'           : 'int',
    'number_last'            : 'int',
    'confidence'             : 'int',
    'level_geocoded_code'    : 'int',
    'gnaf_street_confidence' : 'int',
    'gnaf_reliability_code'  : 'int',
    'planimetric_accuracy'   : 'int',
    'reliability_code'       : 'int',
    'boundary_extent'        : 'int',
    'ps_join_type_code'      : 'int',
    'elevation'              : 'double precision',
    'longitude'              : 'double precision',
    'latitude'               : 'double precision',
}

if not os.path.exists(conf['target_dir'].format(DIR) + conf['source_file']):
    zip_file = urllib2.urlopen(conf['url'])
    with open(conf['source_file'], 'wb+') as output:
        while True:
            data = zip_file.read(4096)
            if data:
                output.write(data)
            else:
                break

with zipfile.ZipFile(conf['target_dir'].format(DIR) + conf['source_file'],"r") as zip_ref:
    zip_ref.extractall(conf['target_dir'].format(DIR) + "extracted")
zip_ref.close()

allowed_localities = [x.strip() for x in conf['localities'].split(',')]

db_engine = models.db_connect()
with db_engine.connect() as connection:
    import_statement_dir = os.path.join( conf['sql_dir'].format(DIR), "import_statements" )
    tables = []

    for fn in glob.glob(conf['target_dir'].format(DIR) + '*/*/*/*/*/*.psv'):
        table = os.path.basename(fn).lower()
        table = table[:table.index('_psv.psv')]

        # Work out the state/territory information for this file
        file_details = table.split('_', 1)
        locality = file_details[0]
        table    = file_details[1]

        # if this is an authority code file we'll need to append the code part
        if locality == 'authority':
            locality = 'authority_code'

        # if it's somewhere we want, or we want all the places,
        # or it's something we need anyway we should create the imports
        if locality in allowed_localities or 'all' in allowed_localities or locality == 'authority_code':
            message = "Processed {} - {}".format( locality, table )

            # Open the source file
            with open(fn, 'r') as f:
                header = f.readline().strip().lower().split('|')
                columns = []
                for col in header:
                    type = type_map['default']
                    if type_map.has_key(col):
                        type = type_map[col]
                    columns.append("{} {}".format(col, type))
                col_list = ', '.join(columns)

                drop_statement   = "drop table if exists {};".format(table)
                create_statement = "create table {} ({});".format(table, col_list)
                write_statement  = "copy {} from '{}' with null '' delimiter '|' csv header;".format(table, fn)

                # If it's not a dry run then import all the data, if it is we'll just generate the .sql files
                # Open the target file, creating it if needed
                filename = os.path.join( import_statement_dir, table + ".sql")
                mode = 'a+'

                new_table = not table in tables
                if new_table:
                    tables.append(table)
                    mode = 'w+'

                with open(filename, mode) as sql_file:
                    if new_table:
                        sql_file.write(drop_statement + "\n")
                        sql_file.write(create_statement + "\n")
                    sql_file.write(write_statement + "\n")

                if not conf['dry_run']:
                    if new_table:
                        connection.execute(text(drop_statement).execution_options(autocommit=True))
                        connection.execute(text(create_statement).execution_options(autocommit=True))
                    connection.execute(text(write_statement).execution_options(autocommit=True))


            #print message

    # build the conglomerate tables
    if not conf['dry_run']:
        with open(os.path.join( conf['sql_dir'].format(DIR), "build_address_detail_flat.sql" ), 'r') as sql_file:
            statement = sql_file.read()
            connection.execute(text(statement).execution_options(autocommit=True))
