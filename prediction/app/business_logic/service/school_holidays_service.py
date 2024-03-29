"""This module handle functions related to the school holidays.
"""
import pandas as pd
from datetime import date
from ..helper.file_helper import get_file_path
import os


fileDir = os.path.dirname(os.path.abspath(__file__))


def dateparse(x):
    """Summary

    Args:
        x (TYPE): Description

    Returns:
        TYPE: Description
    """
    return pd.datetime.strptime(x, '%d.%m.%Y')


def add_new_country_schedule(filename):
    """Summary

    Args:
        filename (TYPE): Description

    Returns:
        TYPE: Description
    """
    df_holidays = reindex_holidays(filename)
    df_holidays = add_region_id(df_holidays)
    df_current_school_holidays = pd.read_csv(get_file_path(
        'data/school_holidays.csv', fileDir), parse_dates=['date'])
    df_current_school_holidays = pd.concate(
        [df_holidays, df_current_school_holidays], axis=0)
    df_current_school_holidays.to_csv('data/school_holidays.csv')


def add_region_id():
    """Merge region with school holidays.

    Returns:
        TYPE: DataFrame
    """
    region = pd.read_csv(get_file_path('data/regions_countries.csv', fileDir))
    holidays = pd.read_csv(get_file_path("data/school_holidays.csv", fileDir),
                           date_parser=dateparse)
    df = pd.merge(holidays[['from_date', 'to_date', 'region_name']],
                  region, on='region_name')
    return df[['region_id', 'from_date', 'to_date']]


def reindex_holidays(filename):
    """Convert a holiday planning file with
    columns "from" & "to" into a list of dates
    with a boolean column "is_holiday"

    Args:
        filename (TYPE): the csv for,at file with field region_id, from, to.

    Returns:
        TYPE: Description
    """
    df_school = pd.read_csv(get_file_path('data/school_holidays/' +
                                          filename + '.csv',
                                          fileDir),
                            parse_dates=['from_date', 'to_date'],
                            date_parser=dateparse)
    date_range = pd.date_range(date(2013, 1, 1), date(2017, 1, 10))
    df_school['from_date2'] = df_school.from_date
    df = df_school.groupby(['region_id']).apply(lambda x: x.set_index(
        'from_date').sort_index().reindex(date_range, method='ffill'))
    df = df.fillna(0)
    df = df.reset_index(level=1)
    df = df.rename(columns={'level_1': 'date', 'from_date2': 'from_date'})
    df['is_holiday'] = (df.date >= df.from_date) & (df.date <= df.to_date)
    df = df[['date', 'is_holiday']]

    return df
