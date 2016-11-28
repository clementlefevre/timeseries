from ..model.merger.counts import CountsMerger
from ..model.merger.weather import WeatherDayMerger
from ..model.merger.public_holidays import PublicHolidaysMerger
from ..model.merger.regions import RegionsMerger


countsMerger = CountsMerger()
weatherDayMerger = WeatherDayMerger()
publicHolidaysMerger = PublicHolidaysMerger()


def merge_all(datastore):
    merged = merge_with_counts(datastore)
    merged = merge_with_weather(datastore, merged)
    merged = merge_with_public_holidays(datastore, merged)
    merged = merge_with_regions(datastore, merged)
    print "datastore.sites_infos", datastore.sites_infos
    return merged


def merge_with_counts(datastore):
    countsMerger.set_datastore(datastore)
    countsMerger.merge_and_clean(datastore.db_manager.sites)
    return countsMerger.merged


def merge_with_weather(datastore, merged):
    if datastore.period == "D":
        weatherDayMerger.set_datastore(datastore)
        weatherDayMerger.merge_and_clean(merged)
        return weatherDayMerger.merged


def merge_with_public_holidays(datastore, merged):
    publicHolidaysMerger.set_datastore(datastore)
    publicHolidaysMerger.merge_and_clean(merged)
    return publicHolidaysMerger.merged


def merge_with_regions(datastore, merged):
    regionsMerger = RegionsMerger()
    regionsMerger.set_datastore(datastore)
    regionsMerger.merge_and_clean(merged)

    return regionsMerger.merged