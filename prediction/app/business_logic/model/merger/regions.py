import app.business_logic.model.merger.abstract as abstract
from app.business_logic.service.geocoding_service import add_region


class RegionsMerger(abstract.Merger):

    def __init__(self):
        super(RegionsMerger, self).__init__(name="regions",
                                            left_keys=['idbldsite'], right_keys=['idbldsite'], suffixes=['', ''])
        self.filter_columns = None

    def _set_right_data(self):
        df_sites = self.datastore.db_manager.sites
        df_sites['customer'] = self.datastore.name
        df_sites = add_region(df_sites)

        self.right = df_sites[['idbldsite', 'region', 'region_id']]

    def _custom(self):
        self.merged = self.merged.drop(['region'], 1)
