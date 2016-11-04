from model.data_store import Data_store
from model.predictor import Predictor
import pandas as pd
import pytest


@pytest.fixture(autouse=True, scope="module")
def store():
    return Data_store(Predictor("DWE_CLOSED_2013", create=True))


def test_create_data_store(store):
    assert store.db.engine is not None


def test_sites_query(store):
    sites = store.db.sites
    assert isinstance(sites, pd.DataFrame)
    assert sites.shape[0] > 0
    assert sites.shape[1] > 0


def test_data_content(store):
    assert store.training_data.shape[0] > 0


def test_geocoding(store):
    assert store.training_data['region_id'].shape[0] > 0
