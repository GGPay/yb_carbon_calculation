import pandas as pd
import logging
from typing import List
import sys
import os


class CarbonAnalitics:
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    def __init__(self):
        self.f_prod = 0.05
        self.mu_purch = 0.5
        self.mu_max_purch = 0.8
        self.file_name = "data.json"
        self.dir_name = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.json_fields = ["ISIN", "Total Energy Use", "Total CO2 Equivalents Emissions",
                            "Renewable Energy Purchased", "Renewable Energy Produced",
                            "Carbon Credit Value", "CO2 Analytic"]

    @staticmethod
    def validate_datasource_fields(datasource_list: List, taget_list: List) -> bool:

        bln_status = False

        datasource_list.sort()
        taget_list.sort()

        if datasource_list == taget_list:
            bln_status = True
        else:
            bln_status = False

        return bln_status

    @staticmethod
    def get_data_from_json(file_name: str, dir_name: str) -> pd.DataFrame:
        try:
            df_data = pd.read_json(os.path.join(dir_name, file_name))

            return df_data
        except (IOError, KeyError) as e:
            CarbonAnalitics.logger.exception(e)
            exit(1)

    def procces_json_data(self, df_data: pd.DataFrame) -> pd.DataFrame:

        df_data.columns = df_data.columns.str.strip().str.lower().str.replace(" ", "_")

        df_data.loc[:, 'f_prod'] = self.f_prod
        df_data.loc[:, 'mu_purch'] = self.mu_purch
        df_data.loc[:, 'mu_max_purch'] = self.mu_max_purch

        return df_data

    def calculate_adjusted_co2_per_company(self):

        CarbonAnalitics.logger.info(f"Start carbon calculation")

        df_data = self.get_data_from_json(self.file_name, self.dir_name)
        if self.validate_datasource_fields(df_data.columns.tolist(), self.json_fields):
            df_data = self.procces_json_data(df_data)
            df_data = self.calculate_co2_tot_minus_cc(df_data)
            df_data = self.calculate_2_component(df_data)
            df_data = self.calculate_co2_adg_total(df_data)
        else:
            CarbonAnalitics.logger.warning(f"Fields in Json file are not the same as in that calculation")

        CarbonAnalitics.logger.info(f"Finish carbon calculation")

    @staticmethod
    def calculate_co2_tot_minus_cc(df_data: pd.DataFrame) -> pd.DataFrame:

        """Calculate 1 component as CO2_tot - CC"""

        df_data["co2_tot_minus_cc"] = df_data['total_co2_equivalents_emissions'] - df_data['carbon_credit_value']

        return df_data

    @staticmethod
    def calculate_2_component(df_data: pd.DataFrame) -> pd.DataFrame:

        """Calculate 2 component as 1 - min (mu_purch * RE_purch/E_tot, mu_max_purch)"""

        df_data["part_component"] = df_data["mu_purch"] * (
                    df_data["renewable_energy_purchased"] / df_data["total_energy_use"])

        df_data["2_component"] = 1 - df_data[['part_component', 'mu_max_purch']].min(axis=1)

        return df_data

    @staticmethod
    def calculate_co2_adg_total(df_data: pd.DataFrame) -> pd.DataFrame:

        """Calculate CO2 adj total by formula"""

        df_data["co2_adg_total"] = df_data["co2_tot_minus_cc"] * df_data["2_component"] - df_data['f_prod'] * df_data[
            'renewable_energy_produced']

        return df_data


if __name__ == "__main__":
    CarbonAnalitics().calculate_adjusted_co2_per_company()
