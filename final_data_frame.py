import pandas as pd
import math

from constants import APARTMENT_TYPES, APARTMENTS_SIZE, C1, C2, COMPETITIVE_FACTOR, CONSTRUCTOR_MOTIVATION_RATIO, CONTRACTORS_AMOUNT, E, EDUCATION_LEVELS_COUNT, EDUCATION_LEVEL_COST, EI, GOVERNMENT_ACTIONS, M, MAX_CONSTRUCTOR_APARTMENTS, MIN_PRICE_DIFF, OPERATIONAL_PROFIT, SI, SUBSIDY_LEVELS, DEMAND_AREAS, TAX_PERCENTAGE, TAX_THRESHOLD, U1, U2
from utils import to_percentage_string

FIELDS = ["Iteration",
          "B Type",
          "Constructor",
          "Land Cost",
          "A type",
          "A Size- Sq.Meters",
          "CC1",
          "CC2",
          "Net OP",
          "Q1",
          "Q2",
          "P1",
          "P2",
          "Primary Action",
          "Subsidy Cost",
          "Education Cost",
          "E",
          "EI",
          "U2-After-Education",
          "U3-After-Education",
          "M2-Education",
          "Quota_M2-Education",
          "Merge_M2-Education",
          "Residual_M2-Education",
          "M1-Education",
          "S",
          "Price Difference",
          "Price Difference- After Subsidy",
          "P2-Subsidized-Relative-Percent",
          "U2-After-Subsidy",
          "M2-After-Subsidy",
          "Quota_M2- Subsidy",
          "Merge_M2- Subsidy",
          "Residual_M2- Subsidy",
          "M1 Subsidy",
          "H1",
          "H2",
          "Constructor Profit"]

def genereate_final_data_frame(land_cost_averages):
  final_data_frame = pd.DataFrame(columns=FIELDS)
  iteration_number = 0
  last_residual_m2_education = 0
  last_residual_m2_subsidy = 0

  education_effects_data_frame = pd.read_csv(r'Education effects.csv')

  for primary_action in list(GOVERNMENT_ACTIONS.keys()):
    for action_level_index in range(GOVERNMENT_ACTIONS[primary_action]):
      if primary_action == "Subsidy":
        subsidy_level = SUBSIDY_LEVELS[action_level_index]
        # TODO: Einav is right - can be more complicated
        subsidy_cost = subsidy_level * M
        # remainder_cost
        education_cost = max(0, E - subsidy_cost)
        education_investment_level = education_cost // EDUCATION_LEVEL_COST
      elif primary_action == "Education":
        education_investment_level = action_level_index
        education_cost = education_investment_level * EDUCATION_LEVEL_COST
        # remainder_cost
        subsidy_cost = max(0, E - education_cost)
        # TODO: Einav is right - type 1 apartments can get susbsidy
        subsidy_level = subsidy_cost // M

      # TODO: It's more realistic to have multiple room apartments per constructor
      for apartment_type in APARTMENT_TYPES:
        for area in DEMAND_AREAS:
          iteration_number += 1
          for constructor_index in range(CONTRACTORS_AMOUNT):
            # Cost calculations
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
            # TODO: Change calculation with the special equation (log... lobbist)
            education_affect = 0.25 / (1 + (math.e ** (-0.5 * (education_investment_level - 7.5))))
            u2_after_education = U2 + education_affect
            m2_education = round(u2_after_education * M) if constructor_index == 0 else last_residual_m2_education
            # TODO: Might need to change this calculation, because it may not be worth for the constructor
            quota_m2_education = min(m2_education, MAX_CONSTRUCTOR_APARTMENTS)
            # (!) We assume here that a constructor will build only a single type of apartments
            merge_m2_education = MAX_CONSTRUCTOR_APARTMENTS \
              if quota_m2_education / MAX_CONSTRUCTOR_APARTMENTS >= CONSTRUCTOR_MOTIVATION_RATIO \
              else 0
            u3_post_education = 1 - u2_after_education - U1
            
            # Subsidy calculations
            subsidized_price_relative_diff_2 = (price_with_tax_2 - price_with_tax_1 - subsidy_level) / price_with_tax_2
            # If the subsidy effect is not significant, the part of "green" demand will be set by the education effects.
            # Otherwise, we'll add to the demand the affected part.
            u2_after_subsidy = u2_after_education \
                if subsidized_price_relative_diff_2 >= MIN_PRICE_DIFF \
                else u2_after_education + SI * u3_post_education
            m2_after_subsidy = round(u2_after_subsidy * M) if constructor_index == 0 else last_residual_m2_subsidy
            quota_m2_subsidy = min(m2_after_subsidy, MAX_CONSTRUCTOR_APARTMENTS)
            merge_m2_subsidy = MAX_CONSTRUCTOR_APARTMENTS \
              if quota_m2_subsidy / MAX_CONSTRUCTOR_APARTMENTS >= CONSTRUCTOR_MOTIVATION_RATIO \
              else 0
            
            # Profit calculations
            apartment_1_profit = round(price_without_tax_1 - total_construction_cost_1)
            apartment_2_profit = round(price_without_tax_2 - total_construction_cost_2)
            h1 = apartment_1_profit * MAX_CONSTRUCTOR_APARTMENTS
            h2 = (apartment_2_profit * merge_m2_subsidy) + (apartment_1_profit * (MAX_CONSTRUCTOR_APARTMENTS - merge_m2_subsidy))

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
              "Primary Action": primary_action,
              "Subsidy Cost": subsidy_cost,
              "Education Cost": education_cost,
              "E": education_investment_level,
              "EI": 0 if education_investment_level == 0 else EI,
              "U2-After-Education": to_percentage_string(u2_after_education),
              "U3-After-Education": to_percentage_string(u3_post_education),
              "M2-Education": m2_education,
              "Quota_M2-Education": quota_m2_education,
              "Merge_M2-Education": merge_m2_education,
              "Residual_M2-Education": 0 if merge_m2_education == 0 else (
                max(m2_education - merge_m2_education, 0)
              ),
              "M1-Education": MAX_CONSTRUCTOR_APARTMENTS - merge_m2_education,
              "S": subsidy_level,
              "Price Difference": round(price_with_tax_2 - price_with_tax_1),
              "Price Difference- After Subsidy": round(price_with_tax_2 - price_with_tax_1 - subsidy_level),
              "P2-Subsidized-Relative-Percent": to_percentage_string(subsidized_price_relative_diff_2),
              "U2-After-Subsidy": to_percentage_string(u2_after_subsidy),
              "M2-After-Subsidy": m2_after_subsidy,
              "Quota_M2- Subsidy": quota_m2_subsidy,
              "Merge_M2- Subsidy": merge_m2_subsidy,
              "Residual_M2- Subsidy": 0 if merge_m2_subsidy == 0 else (
                max(m2_after_subsidy - merge_m2_subsidy, 0)
              ),
              "M1 Subsidy": MAX_CONSTRUCTOR_APARTMENTS - merge_m2_subsidy,
              # "Total M2 Education": ,
              # "Total M1 Education": ,
              # "Total M2 Subsidy": ,
              # "Total M1 Subsidy": ,
              "H1": h1,
              "H2": h2,
              "Constructor Profit": max(h1, h2),
            }
            
            # TODO: Create a list of records and then put it under a dataframe
            new_record_data_frame = pd.DataFrame([record])
            final_data_frame = pd.concat([final_data_frame, new_record_data_frame], ignore_index=True)

            # Data for next iteration
            last_residual_m2_education = 0 if merge_m2_education == 0 else (
                max(m2_education - merge_m2_education, 0)
              )
            last_residual_m2_subsidy = 0 if merge_m2_subsidy == 0 else (
                max(m2_after_subsidy - merge_m2_subsidy, 0)
              )

  return final_data_frame