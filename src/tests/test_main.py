import os
import pandas as pd
import pytest
from yb_carbon_calculation.calculation_model.carbon_analitic import CarbonAnalitics


data_dir = os.path.join(os.path.dirname(__file__), 'data')
file_name = 'test_data.json'

PANDAS_DF_OBJECT = pd.core.frame.DataFrame

json_fields = ["ISIN", "Total Energy Use", "Total CO2 Equivalents Emissions",
               "Renewable Energy Purchased", "Renewable Energy Produced",
               "Carbon Credit Value", "CO2 Analytic"]

json_data = [
              {
                "ISIN": "US0000000006",
                "Total Energy Use": 445000000,
                "Total CO2 Equivalents Emissions": 64963.62994,
                "Renewable Energy Purchased": 9515.906056,
                "Renewable Energy Produced": 24720.73308,
                "Carbon Credit Value": 10556.11359,
                "CO2 Analytic": 53170.89797
              }
            ]


@pytest.fixture(scope="module")
def get_data_from_json(): return CarbonAnalitics.get_data_from_json(file_name, data_dir)


def test_count_class_json_fields():
    ca = CarbonAnalitics()
    assert len(ca.json_fields) == 7


def test_get_data_from_json(get_data_from_json):
    assert isinstance(get_data_from_json, PANDAS_DF_OBJECT)


def test_json_data():
    df_data = CarbonAnalitics().procces_json_data(pd.DataFrame(json_data))
    assert len(df_data.columns) == 10
    assert {'isin', 'total_energy_use', 'total_co2_equivalents_emissions',
            'renewable_energy_purchased', 'renewable_energy_produced',
            'carbon_credit_value', 'co2_analytic',
            'f_prod', 'mu_purch', 'mu_max_purch'}.issubset(
        df_data.columns.tolist())
