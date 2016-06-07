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
import glob
import yaml
import time
import os, sys
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

source_file_path = conf['target_dir'].format(DIR) + conf['source_file']

if not os.path.exists(source_file_path):
    print "Retrieving data source, saving to {}".format(source_file_path)
    zip_file = urllib2.urlopen(conf['url'], timeout=conf['timeout'])
    step     = int(zip_file.info().get('Content-length')) / 100
    download = 0

    sys.stdout.write("{}]".format( " " * 114))
    sys.stdout.write("\rDownloading: [")
    sys.stdout.flush()
    data_chunk = 4096
    with open(conf['source_file'], 'wb+') as output:
        while True:
            data = zip_file.read(data_chunk)
            if data:
                output.write(data)
            else:
                break

            download += data_chunk
            if download >= step:
                sys.stdout.write("=")
                sys.stdout.flush()
                download = 0

with zipfile.ZipFile(source_file_path, "r") as zip_ref:
    print "Extracting data from source"
    zip_ref.extractall(conf['target_dir'].format(DIR) + "extracted")
    print "Extracted."
zip_ref.close()

allowed_localities = [x.strip() for x in conf['localities'].split(',')]

db_engine = models.db_connect()
# Import the data from the .psv files (who uses pipe separators when there's a perfectly good )
with db_engine.connect() as connection:
    import_statement_dir = os.path.join( conf['sql_dir'].format(DIR), "import_statements" )
    tables = []
    locality = None

    for fn in glob.glob(conf['target_dir'].format(DIR) + '*/*/*/*/*/*.psv'):
        table = os.path.basename(fn).lower()
        table = table[:table.index('_psv.psv')]

        # Work out the state/territory information for this file
        file_details = table.split('_', 1)

        if locality != file_details[0]:
            if locality is not None:
                sys.stdout.write('\r\n')
            sys.stdout.write("From {} importing ".format(file_details[0]))

        locality = file_details[0]
        table    = file_details[1]

        sys.stdout.write("{}, ".format(table))
        sys.stdout.flush()

        # if it's somewhere we want, or we want all the places,
        # or it's something we need anyway we should create the imports
        if locality in allowed_localities or 'all' in allowed_localities or locality == 'authority':
            # Open the source file
            with open(fn, 'r') as f:
                # read through the header to get the columns
                header = f.readline().strip().lower().split('|')
                columns = []
                for col in header:
                    type = type_map['default']
                    if type_map.has_key(col):
                        type = type_map[col]
                    columns.append("{} {}".format(col, type))
                col_list = ', '.join(columns)

                # work out if we have a new table on our hands, and set the appropriate file mode
                mode = 'a+'
                statements = []

                if not table in tables:
                    tables.append(table)
                    mode = 'w+'
                    statements.append("drop table if exists {} cascade;".format(table))
                    statements.append("create table {} ({});".format(table, col_list))

                statements.append("copy {} from '{}' with null '' delimiter '|' csv header;".format(table, fn))

                # If it's not a dry run then import all the data, if it is we'll just generate the .sql files
                filename = os.path.join( import_statement_dir, table + ".sql")
                with open(filename, mode) as sql_file:
                    for statement in statements:
                        sql_file.write(statement + "\n")

                if not conf['dry_run']:
                    for statement in statements:
                        connection.execute(text(statement).execution_options(autocommit=True))

    print "\r\nImport complete."

    statement = models.get_addresses_statement()
    print "Creating new addresses view"
    # Create the table from the imported data
    connection.execute(text(statement).execution_options(autocommit=True))
    print "Done."
    # close the connection as we're done
    connection.close()
