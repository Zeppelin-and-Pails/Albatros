# Albatros
A Python based API for accessing the Australian GNAF dataset

# G-NAF
Geocoded National Address File is Australia’s authoritative, geocoded address file.   
this tool will load a subset of the GNAF into a combined "addresses" table for accessing via an API

# Prerequisites

 - Working PostgreSQL instalation   
 - A user with the superuser role for the import   
 - A few python packages (see require)

# Import data

 - Add the appropriate database details to Albatros/api/db.cfg   
 - Update data_importer.cfg with the desired settings   
 - Run Albatros/data_importer.py   

# Addresses View

This view combines additional address information from address component tables into the `address_detail`.   
Appendix B in the [G-NAF documentation](https://www.psma.com.au/sites/default/files/g-naf_product_description.pdf) describes the rest of the data model in detail.

```
                   View "addresses"
             Column             |       Type       
--------------------------------+------------------
 address_detail_pid             | text             
 building_name                  | text             
 lot_number_prefix              | text             
 lot_number                     | text             
 lot_number_suffix              | text             
 flat_type_code                 | text             
 flat_number_prefix             | text             
 flat_number                    | integer          
 flat_number_suffix             | text             
 level_type_code                | text             
 level_number_prefix            | text             
 level_number                   | integer          
 level_number_suffix            | text             
 number_first_prefix            | text             
 number_first                   | integer          
 number_first_suffix            | text             
 number_last_prefix             | text             
 number_last                    | integer          
 number_last_suffix             | text             
 location_description           | text             
 alias_principal                | text             
 postcode                       | text             
 private_street                 | text             
 legal_parcel_id                | text             
 confidence                     | integer          
 level_geocoded_code            | integer          
 property_pid                   | text             
 gnaf_property_pid              | text             
 primary_secondary              | text             
 mb_2011_code                   | text             
 mb_match_code                  | text             
 street_class_code              | text             
 street_name                    | text             
 street_type_code               | text             
 street_suffix_code             | text             
 gnaf_street_pid                | text             
 gnaf_street_confidence         | integer          
 street_gnaf_reliability_code   | integer          
 locality_name                  | text             
 primary_postcode               | text             
 locality_class_code            | text             
 gnaf_locality_pid              | text             
 locality_gnaf_reliability_code | integer          
 state_abbreviation             | text             
 locality_planimetric_accuracy  | integer          
 locality_longitude             | double precision 
 locality_latitude              | double precision 
 address_type                   | text             
 address_site_name              | text             
 geocode_type_code              | text             
 longitude                      | double precision 
 latitude                       | double precision 
 boundary_extent                | integer          
 street_planimetric_accuracy    | integer          
 street_longitude               | double precision 
 street_latitude                | double precision 
```

The following tables are included in the import:
```
                Name                 | Type  |  Owner   
-------------------------------------+-------+----------
 address_alias                       | table | albatros
 address_default_geocode             | table | albatros
 address_detail                      | table | albatros
 address_mesh_block_2011             | table | albatros
 address_site                        | table | albatros
 address_site_geocode                | table | albatros
 addresses                           | table | albatros
 code_address_alias_type_aut         | table | albatros
 code_address_type_aut               | table | albatros
 code_flat_type_aut                  | table | albatros
 code_geocode_reliability_aut        | table | albatros
 code_geocode_type_aut               | table | albatros
 code_geocoded_level_type_aut        | table | albatros
 code_level_type_aut                 | table | albatros
 code_locality_alias_type_aut        | table | albatros
 code_locality_class_aut             | table | albatros
 code_mb_match_code_aut              | table | albatros
 code_ps_join_type_aut               | table | albatros
 code_street_class_aut               | table | albatros
 code_street_locality_alias_type_aut | table | albatros
 code_street_suffix_aut              | table | albatros
 code_street_type_aut                | table | albatros
 locality                            | table | albatros
 locality_alias                      | table | albatros
 locality_neighbour                  | table | albatros
 locality_point                      | table | albatros
 mb_2011                             | table | albatros
 primary_secondary                   | table | albatros
 state                               | table | albatros
 street_locality                     | table | albatros
 street_locality_alias               | table | albatros
 street_locality_point               | table | albatros
 ```