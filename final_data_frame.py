import pandas as pd

from constants import APARTMENT_TYPES, APARTMENTS_SIZE, C1, C2, COMPETITIVE_FACTOR, CONTRACTORS_AMOUNT, EDUCATION_INVESTMENT_LEVELS, EI, OPERATIONAL_PROFIT, SUBSIDY_LEVELS, DEMAND_AREAS, TAX_PERCENTAGE, TAX_THRESHOLD, U2
from utils import to_percentage_string

FIELDS = ["Iteration", "B Type", "Constructor", "Land Cost", "A type",
          "A Size- Sq.Meters", "CC1", "CC2", "Net OP", "Q1", "Q2", "P1",
          "P2", "E", "EI", "U2-Education",
          "U3-Education", "M2-Education", "Quota_M2-Education",
          "Merge_M2-Education", "Residual_M2-Education", "M1-Education",
          "S", "SI", "Price Difference", "Price Difference- After Subsidy",
          "Percent", "U2- Subsidy", "M2- Subsidy", "Quota_M2- Subsidy",
          "Merge_M2- Subsidy", "Residual_M2- Subsidy", "M1 Subsidy",
          "Total M2 Education", "Total M1 Education", "Total M2 Subsidy",
          "Total M1 Subsidy"]

def genereate_final_data_frame(land_cost_averages):
  final_data_frame = pd.DataFrame(columns=FIELDS)
  iteration_number = 0

  for subsidy_level in SUBSIDY_LEVELS:
    for education_investment_level in EDUCATION_INVESTMENT_LEVELS:
      for apartment_type in APARTMENT_TYPES:
        for area in DEMAND_AREAS:
          iteration_number += 1
          for constructor_index in range(CONTRACTORS_AMOUNT):
            land_cost = land_cost_averages[area]
            apartment_size = APARTMENTS_SIZE[apartment_type]
            total_construction_cost_1 = apartment_size * C1 + land_cost
            total_construction_cost_2 = apartment_size * C2 + land_cost
            net_operational_profit = OPERATIONAL_PROFIT - (constructor_index * COMPETITIVE_FACTOR)
            price_without_tax_1 = total_construction_cost_1 * (net_operational_profit + 1)
            price_without_tax_2 = total_construction_cost_2 * (net_operational_profit + 1)

            record = {
              "Iteration": iteration_number,
              "B Type": area,
              "Constructor": constructor_index + 1,
              "Land Cost": land_cost,
              "A type": apartment_type,
              "A Size- Sq.Meters": apartment_size,
              "CC1": total_construction_cost_1,
              "CC2": total_construction_cost_2,
              "Net OP": to_percentage_string(net_operational_profit),
              "Q1": price_without_tax_1,
              "Q2": price_without_tax_2,
              "P1": (price_without_tax_1 - TAX_THRESHOLD) * TAX_PERCENTAGE + price_without_tax_1 \
                if price_without_tax_1 > TAX_THRESHOLD else price_without_tax_1,
              "P2": (price_without_tax_2 - TAX_THRESHOLD) * TAX_PERCENTAGE + price_without_tax_2 \
                if price_without_tax_2 > TAX_THRESHOLD else price_without_tax_2,
              "E": education_investment_level,
              "EI": 0 if education_investment_level == 0 else EI,
              # -------------
              # =((1.05^6)-1)*(C41)+B18
              "U2-Education": to_percentage_string((1.05 ** education_investment_level - 1) *  + U2),
              "U3-Education": 290,
              "M2-Education": 300,
              "Quota_M2-Education": 310,
              "Merge_M2-Education": 320,
              "Residual_M2-Education": 330,
              "M1-Education": 340,
              "S": 350,
              "SI": 360,
              "Price Difference": 370,
              "Price Difference- After Subsidy": 380,
              "Percent": 390,
              "U2- Subsidy": 400,
              "M2- Subsidy": 410,
              "Quota_M2- Subsidy": 420,
              "Merge_M2- Subsidy": 430,
              "Residual_M2- Subsidy": 440,
              "M1 Subsidy": 450,
              "Total M2 Education": 460,
              "Total M1 Education": 470,
              "Total M2 Subsidy": 480,
              "Total M1 Subsidy": 490,
            }
            
            df = df.append(record, ignore_index=True)

  return final_data_frame