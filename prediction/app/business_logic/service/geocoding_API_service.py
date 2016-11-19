"""Summary

Attributes:
    MAPS_URL (TYPE): Description
"""
import os
import urllib2
import json
import pandas as pd
import logging
import inspect
from ..model.config_manager import Config_manager
from ..helper.data_helper import check_missing_data
from ..helper.file_helper import get_file_path


config_manager = Config_manager()

fileDir = os.path.dirname(os.path.abspath(__file__))


def get_region(latitude, longitude):
    """retrieve the local name of the region for a given coordinate.

    Args:
        latitude (int):
        longitude (int):

    Returns:
        str: local name of the region
    """

    MAPS_URL = config_manager.geocoding_API['maps_url']
    KEY = config_manager.geocoding_API['key']

    coord_str = str(latitude) + "," + str(longitude)
    try:
        response = urllib2.urlopen(
            MAPS_URL + coord_str + "&key=" + KEY)
        data = json.loads(response.read())
        address_components = data['results'][0]['address_components']

        region = [x for x in address_components
                  if 'administrative_area_level_1' in x[
                      'types']][0]['long_name'].encode('utf-8)')
        return region
    except (AttributeError, IndexError) as e:
        logging.error("Could not retrieve the region name for :" + coord_str)
        logging.error(e.message)


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
    df_region_id = pd.read_csv(get_file_path(
        'data/regions_countries.csv', fileDir))

    df_sites = pd.merge(df_sites, df_region_id, on='region', how='left',
                        indicator=True)

    df_sites = check_missing_data(df_sites,
                                  "left_only",
                                  inspect.currentframe().f_code.co_name, drop_missing=False)

    df_sites = df_sites[['idbldsite', 'sname', 'latitude', 'longitude',
                         'region', 'region_id']]
    datastore.sites_infos = df_sites

    return df_sites[['idbldsite', 'region', 'region_id']]