create or replace view addresses as
  select
    address_detail.address_detail_pid
    , address_detail.building_name
    , address_detail.lot_number_prefix
    , address_detail.lot_number
    , address_detail.lot_number_suffix
    , address_detail.flat_type_code
    , address_detail.flat_number_prefix
    , address_detail.flat_number
    , address_detail.flat_number_suffix
    , address_detail.level_type_code
    , address_detail.level_number_prefix
    , address_detail.level_number
    , address_detail.level_number_suffix
    , address_detail.number_first_prefix
    , address_detail.number_first
    , address_detail.number_first_suffix
    , address_detail.number_last_prefix
    , address_detail.number_last
    , address_detail.number_last_suffix
    , address_detail.location_description
    , address_detail.alias_principal
    , address_detail.postcode
    , address_detail.private_street
    , address_detail.legal_parcel_id
    , address_detail.confidence
    , address_detail.level_geocoded_code
    , address_detail.property_pid
    , address_detail.gnaf_property_pid
    , address_detail.primary_secondary
    , mb_2016.mb_2016_code
    , address_mesh_block_2016.mb_match_code
    , street_locality.street_class_code
    , street_locality.street_name
    , street_locality.street_type_code
    , street_locality.street_suffix_code
    , street_locality.gnaf_street_pid
    , street_locality.gnaf_street_confidence
    , street_locality.gnaf_reliability_code as street_gnaf_reliability_code
    , locality.locality_name
    , locality.primary_postcode
    , locality.locality_class_code
    , locality.gnaf_locality_pid
    , locality.gnaf_reliability_code as locality_gnaf_reliability_code
    , state.state_abbreviation
    , locality_point.planimetric_accuracy as locality_planimetric_accuracy
    , locality_point.longitude as locality_longitude
    , locality_point.latitude as locality_latitude
    , address_site.address_type
    , address_site.address_site_name
    , address_default_geocode.geocode_type_code
    , address_default_geocode.longitude as longitude
    , address_default_geocode.latitude as latitude
    , street_locality_point.boundary_extent as boundary_extent
    , street_locality_point.planimetric_accuracy as street_planimetric_accuracy
    , street_locality_point.longitude as street_longitude
    , street_locality_point.latitude as street_latitude
  from address_detail
    left outer join address_mesh_block_2016 on address_mesh_block_2016.address_detail_pid = address_detail.address_detail_pid
    left outer join mb_2016 on mb_2016.mb_2016_pid = address_mesh_block_2016.mb_2016_pid
    left outer join address_site on address_site.address_site_pid = address_detail.address_site_pid
    left outer join locality on locality.locality_pid = address_detail.locality_pid
    left outer join street_locality on street_locality.street_locality_pid = address_detail.street_locality_pid
    left outer join state on state.state_pid = locality.state_pid
    left outer join locality_point on locality_point.locality_pid = locality.locality_pid
    left outer join address_default_geocode on address_default_geocode.address_detail_pid = address_detail.address_detail_pid
    left outer join street_locality_point on street_locality_point.street_locality_pid = street_locality.street_locality_pid
;

/*
-- Setup a conglomerate table containing all the details, rather than the view
drop table if exists addresses;
create table addresses as
select
    address_detail.address_detail_pid
  , address_detail.building_name
  , address_detail.lot_number_prefix
  , address_detail.lot_number
  , address_detail.lot_number_suffix
  , address_detail.flat_type_code
  , address_detail.flat_number_prefix
  , address_detail.flat_number
  , address_detail.flat_number_suffix
  , address_detail.level_type_code
  , address_detail.level_number_prefix
  , address_detail.level_number
  , address_detail.level_number_suffix
  , address_detail.number_first_prefix
  , address_detail.number_first
  , address_detail.number_first_suffix
  , address_detail.number_last_prefix
  , address_detail.number_last
  , address_detail.number_last_suffix
  , address_detail.location_description
  , address_detail.alias_principal
  , address_detail.postcode
  , address_detail.private_street
  , address_detail.legal_parcel_id
  , address_detail.confidence
  , address_detail.level_geocoded_code
  , address_detail.property_pid
  , address_detail.gnaf_property_pid
  , address_detail.primary_secondary
  , mb_2016.mb_2016_code
  , address_mesh_block_2016.mb_match_code
  , street_locality.street_class_code
  , street_locality.street_name
  , street_locality.street_type_code
  , street_locality.street_suffix_code
  , street_locality.gnaf_street_pid
  , street_locality.gnaf_street_confidence
  , street_locality.gnaf_reliability_code as street_gnaf_reliability_code
  , locality.locality_name
  , locality.primary_postcode
  , locality.locality_class_code
  , locality.gnaf_locality_pid
  , locality.gnaf_reliability_code as locality_gnaf_reliability_code
  , state.state_abbreviation
  , locality_point.planimetric_accuracy as locality_planimetric_accuracy
  , locality_point.longitude as locality_longitude
  , locality_point.latitude as locality_latitude
  , address_site.address_type
  , address_site.address_site_name
  , address_default_geocode.geocode_type_code
  , address_default_geocode.longitude as longitude
  , address_default_geocode.latitude as latitude
  , street_locality_point.boundary_extent as boundary_extent
  , street_locality_point.planimetric_accuracy as street_planimetric_accuracy
  , street_locality_point.longitude as street_longitude
  , street_locality_point.latitude as street_latitude
from address_detail
  left outer join address_mesh_block_2016 on address_mesh_block_2016.address_detail_pid = address_detail.address_detail_pid
  left outer join mb_2016 on mb_2016.mb_2016_pid = address_mesh_block_2016.mb_2016_pid
  left outer join address_site on address_site.address_site_pid = address_detail.address_site_pid
  left outer join locality on locality.locality_pid = address_detail.locality_pid
  left outer join street_locality on street_locality.street_locality_pid = address_detail.street_locality_pid
  left outer join state on state.state_pid = locality.state_pid
  left outer join locality_point on locality_point.locality_pid = locality.locality_pid
  left outer join address_default_geocode on address_default_geocode.address_detail_pid = address_detail.address_detail_pid
  left outer join street_locality_point on street_locality_point.street_locality_pid = street_locality.street_locality_pid
;

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
drop table if exists address_mesh_block_2016;
drop table if exists mb_2016;
*/