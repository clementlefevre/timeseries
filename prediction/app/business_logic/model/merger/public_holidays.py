import app.business_logic.model.merger.abstract as abstract


class PublicHolidaysMerger(abstract.Merger):

    def __init__(self):
        super(PublicHolidaysMerger, self).__init__(name="public_holidays",
                                                   left_keys=['idbldsite',
                                                              'date'], right_keys=['idbldsite', 'day'],
                                                   how='left', suffixes=['_counts', '_holidays'],
                                                   drop_missing=False)
        self.filter_columns = ['idbldsite', 'compensatedin', 'date',
                               'date_time', 'maxtemperature', 'mintemperature',
                               'weathersituation', 'cloudamount', 'is_public_holiday']

    def _set_right_data(self):
        self.right = self.datastore.db_manager.public_holidays[
            ['idbldsite', 'day']]
        self.right.day = abstract.pd.to_datetime(self.right.day)

    def _custom(self):
        self.merged['is_public_holiday'] = ~self.merged.day.isnull() * 1
