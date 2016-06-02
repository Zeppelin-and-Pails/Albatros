-- Setup the conglomerate table containing all the details you would normally want
drop table if exists address_detail_flat;
create table address_detail_flat as
select
    ad.address_detail_pid
  , ad.building_name
  , ad.lot_number_prefix
  , ad.lot_number
  , ad.lot_number_suffix
  , ad.flat_type_code
  , ad.flat_number_prefix
  , ad.flat_number
  , ad.flat_number_suffix
  , ad.level_type_code
  , ad.level_number_prefix
  , ad.level_number
  , ad.level_number_suffix
  , ad.number_first_prefix
  , ad.number_first
  , ad.number_first_suffix
  , ad.number_last_prefix
  , ad.number_last
  , ad.number_last_suffix
  , ad.location_description
  , ad.alias_principal
  , ad.postcode
  , ad.private_street
  , ad.legal_parcel_id
  , ad.confidence
  , ad.level_geocoded_code
  , ad.property_pid
  , ad.gnaf_property_pid
  , ad.primary_secondary
  , m2.mb_2011_code
  , amb2.mb_match_code
  , sl.street_class_code
  , sl.street_name
  , sl.street_type_code
  , sl.street_suffix_code
  , sl.gnaf_street_pid
  , sl.gnaf_street_confidence
  , sl.gnaf_reliability_code street_gnaf_reliability_code
  , l.locality_name
  , l.primary_postcode
  , l.locality_class_code
  , l.gnaf_locality_pid
  , l.gnaf_reliability_code locality_gnaf_reliability_code
  , s.state_abbreviation
  , lp.planimetric_accuracy locality_planimetric_accuracy
  , lp.longitude locality_longitude
  , lp.latitude locality_latitude
  , site.address_type
  , site.address_site_name
  , adg.geocode_type_code
  , adg.longitude longitude
  , adg.latitude latitude
  , slp.boundary_extent boundary_extent
  , slp.planimetric_accuracy street_planimetric_accuracy
  , slp.longitude street_longitude
  , slp.latitude street_latitude
from address_detail ad
left outer join address_mesh_block_2011 amb2 on amb2.address_detail_pid = ad.address_detail_pid
left outer join mb_2011 m2 on m2.mb_2011_pid = amb2.mb_2011_pid
left outer join address_site site on site.address_site_pid = ad.address_site_pid
left outer join locality l on l.locality_pid = ad.locality_pid
left outer join street_locality sl on sl.street_locality_pid = ad.street_locality_pid
left outer join state s on s.state_pid = l.state_pid
left outer join locality_point lp on lp.locality_pid = l.locality_pid
left outer join address_default_geocode adg on adg.address_detail_pid = ad.address_detail_pid
left outer join street_locality_point slp on slp.street_locality_pid = sl.street_locality_pid
;

/*
-- Drop all the tables used to build the conglomerate
drop table if exists address_detail;
drop table if exists address_site;
drop table if exists street_locality;
drop table if exists address_alias;
drop table if exists street_locality_alias;
drop table if exists address_alias;
drop table if exists street_locality_alias;
drop table if exists locality_neighbour;
drop table if exists locality_alias;
drop table if exists locality_point;
drop table if exists address_default_geocode;
drop table if exists address_site_geocode;
drop table if exists street_locality_point;
drop table if exists primary_secondary;
drop table if exists address_mesh_block_2011;
drop table if exists mb_2011;
*/