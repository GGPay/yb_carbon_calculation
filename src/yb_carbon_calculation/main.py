from yb_carbon_calculation.calculation_model.carbon_analitic import CarbonAnalitics


def run_carbon_analytics():
    CarbonAnalitics().calculate_adjusted_co2_per_company()
