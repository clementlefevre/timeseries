"""Summary

Attributes:
    MAPS_URL (TYPE): Description
"""
import urllib2
import json
import pandas as pd


MAPS_URL = "http://maps.googleapis.com/maps/api/geocode/json?latlng="


def get_region(latitude, longitude):
    """retrieve the local name of the region for a given coordinate.

    Args:
        latitude (int):
        longitude (int):

    Returns:
        str: local name of the region
    """
    coord_str = str(latitude) + "," + str(longitude)
    try:
        response = urllib2.urlopen(
            MAPS_URL + coord_str)
        data = json.loads(response.read())
        address_components = data['results'][0]['address_components']

        region = [x for x in address_components if 'administrative_area_level_1' in x[
            'types']][0]['long_name'].encode('utf-8)')
        
        return region
    except Exception as e:
        print e.message

        print "Could not retrieve the region name for :" + coord_str
        raise


def create_regions_df(datastore):
    """create a dataframe of sites with the corresponding local region name.

    Args:
        datastore (DataFrame):

    Returns:
        DataFrame: sites-regions
    """
    df_sites = datastore.db.sites
    df_sites['region'] = df_sites.apply(
        lambda row: get_region(row['latitude'], row['longitude']), axis=1)

    df_region_id = pd.read_csv('data/region_germany.csv')
    df_sites = pd.merge(df_sites, df_region_id, on='region', how='left')
    datastore.db.sites = df_sites
    df_sites = df_sites[['idbldsite', 'sname', 'latitude', 'longitude',
                         'coord', 'region', 'region_id']]
    df_sites.to_csv(datastore.config.data_store_settings[
        'path'] + '/' + datastore.config.DB['db_name'] + '_' + 'sites_infos' + '.csv', encoding='utf-8')

    return df_sites[['idbldsite', 'region', 'region_id']]
