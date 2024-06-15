import pandas as pd

from constants import DEMAND_AREAS
from df_kdd import calculate_region_average_apartment_price
from final_data_frame import genereate_final_data_frame


def main():
    input_data_frame = pd.read_csv(
        r'Leed game theory calculations - Lands Value database.csv')

    land_cost_averages = {}
    for area in DEMAND_AREAS:
        land_cost_averages[area] = calculate_region_average_apartment_price(
            input_data_frame, area)

    final_data_frame = genereate_final_data_frame(land_cost_averages)
    final_data_frame
    final_data_frame.to_csv('output.csv')


if __name__ == "__main__":
    main()
