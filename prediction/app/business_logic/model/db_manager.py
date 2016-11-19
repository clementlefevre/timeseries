import os
from sqlalchemy import create_engine
from ..model import pd, logging
from ..helper.file_helper import get_file_path

fileDir = os.path.dirname(os.path.abspath(__file__))


class DB_manager(object):

    def __init__(self, db_params):
        self.params = db_params
        self._create_connection()
        self._init_data()

    def _db_address(self):

        credentials = self.params['db_user'] + ':' + self.params['db_pwd']
        address = 'postgresql://' + credentials + '@' + \
            self.params['db_url'] + ':' + \
            self.params['db_port'] + '/' + self.params['db_name']
        return address

    def _create_connection(self):
        self.engine = create_engine(self._db_address())
        logging.info("engine created : " + str(self.engine))

    def _query(self, table):
        return pd.read_sql_query("select * from " + '"' + table + '"',
                                 con=self.engine)

    def _init_data(self):
        self.sites = self._query("dwe_bld_site")
        self.counts = self._query("dwe_cnt_site")
        self.addresses = self._query("dwe_bld_address")
        self.weather_day = self._query("dwe_ext_weather_meteogroup_day")
        self.weather_intraday = self._query(
            "dwe_ext_weather_meteogroup_intraday")
        self.public_holidays = self._query("dwe_cal_holiday")
        filename = get_file_path(
            "data/store/" + self.params['db_name'] + "_public_holidays.csv", fileDir)
        filename = os.path.abspath(os.path.realpath(filename))

        self.public_holidays.to_csv(filename, sep=";", encoding="utf-8")
        self.conversion = self._query("dwe_ext_conversion")