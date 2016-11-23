import os
import pandas as pd
from datetime import datetime
from ..helper.file_helper import get_file_path

fileDir = os.path.dirname(os.path.abspath(__file__))


def merge_with_conversion(datastore):
    if datastore.period == 'H':
        return add_conversion_hour(datastore)

    if datastore.period == 'D':
        return add_conversion_day(datastore)


def add_conversion_hour(datastore):
    merged = pd.merge(datastore.training_data, datastore.db.conversion, left_on=['idbldsite', 'date_time'],
                      right_on=['idbldsite', 'timefrom'], how='left')

    merged = merged.drop(['id', 'timefrom', 'timeto'], 1)
    return merged


def add_conversion_day(datastore):
    df_conversion_day = get_conversion_day(datastore)
    merged = pd.merge(datastore.training_data, df_conversion_day, left_on=['idbldsite', 'date'],
                      right_on=['idbldsite', 'date'], how='left')
    merged = merged.drop('id', 1)
    merged.to_csv(get_file_path("data/conversion_day.csv", fileDir))
    return merged


def get_conversion(datastore):
    df_conversion = pd.DataFrame()
    if datastore.period == 'D':
        df_conversion = get_conversion_day(datastore)
    elif datastore.period == 'H':
        df_conversion = datastore.db.conversion

    return df_conversion


def get_conversion_day(datastore):
    df_conversion_day = datastore.db.conversion
    df_conversion_day['date'] = df_conversion_day['timefrom'].apply(
        lambda dt: datetime(dt.year, dt.month, dt.day))
    df_conversion_day = df_conversion_day.groupby(
        ['idbldsite', 'date']).sum()
    df_conversion_day = df_conversion_day.reset_index()
    return df_conversion_day
