import pandas as pd

from constants import APARTMENT_TYPES, APARTMENTS_SIZE, C1, C2, COMPETITIVE_FACTOR, CONSTRUCTOR_MOTIVATION_RATIO, CONTRACTORS_AMOUNT, EDUCATION_INVESTMENT_LEVELS, EI, M, MAX_CONSTRUCTOR_APARTMENTS, MIN_PRICE_DIFF, OPERATIONAL_PROFIT, SI, SUBSIDY_LEVELS, DEMAND_AREAS, TAX_PERCENTAGE, TAX_THRESHOLD, U1, U2
from utils import to_percentage_string

FIELDS = ["Iteration", "B Type", "Constructor", "Land Cost", "A type",
          "A Size- Sq.Meters", "CC1", "CC2", "Net OP", "Q1", "Q2", "P1",
          "P2", "E", "EI", "U2-Education",
          "U3-Education", "M2-Education", "Quota_M2-Education",
          "Merge_M2-Education", "Residual_M2-Education", "M1-Education",
          "S", "SI", "Price Difference", "Price Difference- After Subsidy",
          "Percent", "U2- Subsidy", "M2- Subsidy", "Quota_M2- Subsidy",
          "Merge_M2- Subsidy", "Residual_M2- Subsidy", "M1 Subsidy"]

def genereate_final_data_frame(land_cost_averages):
  final_data_frame = pd.DataFrame(columns=FIELDS)
  iteration_number = 0
  last_residual_m2_education = 0
  last_residual_m2_subsidy = 0

  education_effects_data_frame = pd.read_csv(r'Education effects.csv')

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
            price_with_tax_1 = (price_without_tax_1 - TAX_THRESHOLD) * TAX_PERCENTAGE + price_without_tax_1 \
              if price_without_tax_1 > TAX_THRESHOLD else price_without_tax_1
            price_without_tax_2 = total_construction_cost_2 * (net_operational_profit + 1)
            price_with_tax_2 = (price_without_tax_2 - TAX_THRESHOLD) * TAX_PERCENTAGE + price_without_tax_2 \
                if price_without_tax_2 > TAX_THRESHOLD else price_without_tax_2
            
            # Education calculations
            u2_education = education_effects_data_frame.loc[
                  education_effects_data_frame['i'] == education_investment_level, 'U2(i)'
                ].values[0] / 100
            m2_education = round(u2_education * M) if constructor_index == 0 else last_residual_m2_education
            quota_m2_education = min(m2_education, MAX_CONSTRUCTOR_APARTMENTS)
            merge_m2_education = MAX_CONSTRUCTOR_APARTMENTS \
              if quota_m2_education / MAX_CONSTRUCTOR_APARTMENTS >= CONSTRUCTOR_MOTIVATION_RATIO \
              else 0
            u3_education = 1 - u2_education - U1
            
            # Subsidy calculations
            si_value = SI if subsidy_level > 0 else 0
            price_relative_diff = (price_with_tax_2 - price_with_tax_1 - subsidy_level) / price_with_tax_2
            u2_subsidy = to_percentage_string(u2_education) \
                if price_relative_diff >= MIN_PRICE_DIFF \
                else u2_education + si_value * u3_education
            m2_subsidy = round(u2_education * M) if constructor_index == 0 else last_residual_m2_subsidy
            quota_m2_subsidy = min(m2_subsidy, MAX_CONSTRUCTOR_APARTMENTS)
            merge_m2_subsidy = MAX_CONSTRUCTOR_APARTMENTS \
              if quota_m2_subsidy / MAX_CONSTRUCTOR_APARTMENTS >= CONSTRUCTOR_MOTIVATION_RATIO \
              else 0

            record = {
              "Iteration": iteration_number,
              "B Type": area,
              "Constructor": constructor_index + 1,
              "Land Cost": land_cost,
              "A type": apartment_type,
              "A Size- Sq.Meters": apartment_size,
              "CC1": round(total_construction_cost_1),
              "CC2": round(total_construction_cost_2),
              "Net OP": to_percentage_string(net_operational_profit),
              "Q1": round(price_without_tax_1),
              "Q2": round(price_without_tax_2),
              "P1": round(price_with_tax_1),
              "P2": round(price_with_tax_2),
              "E": education_investment_level,
              "EI": 0 if education_investment_level == 0 else EI,
              "U2-Education": to_percentage_string(u2_education),
              "U3-Education": to_percentage_string(u3_education),
              "M2-Education": to_percentage_string(m2_education),
              "Quota_M2-Education": quota_m2_education,
              "Merge_M2-Education": merge_m2_education,
              "Residual_M2-Education": 0 if merge_m2_education == 0 else (
                max(m2_education - merge_m2_education, 0)
              ),
              "M1-Education": MAX_CONSTRUCTOR_APARTMENTS - merge_m2_education,
              "S": subsidy_level,
              "SI": si_value,
              "Price Difference": round(price_with_tax_2 - price_with_tax_1),
              "Price Difference- After Subsidy": round(price_with_tax_2 - price_with_tax_1 - subsidy_level),
              "Percent": to_percentage_string(price_relative_diff),
              "U2- Subsidy": u2_subsidy,
              "M2- Subsidy": m2_subsidy,
              "Quota_M2- Subsidy": quota_m2_subsidy,
              "Merge_M2- Subsidy": merge_m2_subsidy,
              "Residual_M2- Subsidy": 0 if merge_m2_subsidy == 0 else (
                max(m2_subsidy - merge_m2_subsidy, 0)
              ),
              "M1 Subsidy": MAX_CONSTRUCTOR_APARTMENTS - merge_m2_subsidy,
              # "Total M2 Education": ,
              # "Total M1 Education": ,
              # "Total M2 Subsidy": ,
              # "Total M1 Subsidy": ,
            }
            
            # TODO: Create a list of records and then put it under a dataframe
            new_record_data_frame = pd.DataFrame([record])
            final_data_frame = pd.concat([final_data_frame, new_record_data_frame], ignore_index=True)

            # Data for next iteration
            last_residual_m2_education = 0 if merge_m2_education == 0 else (
                max(m2_education - merge_m2_education, 0)
              )
            last_residual_m2_subsidy = 0 if merge_m2_subsidy == 0 else (
                max(m2_subsidy - merge_m2_subsidy, 0)
              )

  return final_data_frame