import pandas as pd
import math

from constants import APARTMENTS_DETAILS, C1, C2, COMPETITIVE_FACTOR, CONSTRUCTOR_MOTIVATION_RATIO, CONTRACTORS_AMOUNT, E, EDUCATION_LEVELS_COUNT, EDUCATION_LEVEL_COST, EI, GOVERNMENT_ACTIONS, M, MAX_CONSTRUCTOR_APARTMENTS, MIN_PRICE_DIFF, OPERATIONAL_PROFIT, SI, SUBSIDY_LEVELS, DEMAND_AREAS, TAX_PERCENTAGE, TAX_THRESHOLD, U1, U2
from utils import to_percentage_string

FIELDS = ["Iteration",
          "B Type",
          "Constructor",
          "Land Cost",
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

# TODO1: Solve number of rooms problem 
# TODO2: Make the constructor build the scenario which makes him the highest profit
def genereate_final_data_frame(land_cost_averages):
  final_data_frame = pd.DataFrame(columns=FIELDS)
  iteration_number = 0
  last_residual_m2_education = 0
  last_residual_m2_subsidy = 0

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

      # Education calculations
      education_affect = 0.25 / (1 + (math.e ** (-0.5 * (education_investment_level - 7.5))))
      u2_after_education = U2 + education_affect
      u3_post_education = 1 - u2_after_education - U1

      for area in DEMAND_AREAS:
        iteration_number += 1
        for constructor_index in range(CONTRACTORS_AMOUNT):
          total_summary = {}

          # Cost calculations
          land_cost = land_cost_averages[area]
          net_operational_profit = OPERATIONAL_PROFIT - (constructor_index * COMPETITIVE_FACTOR)

          total_construction_cost_1 = 0
          total_construction_cost_2 = 0
          u2_after_subsidy = u2_after_education
          h1 = 0
          for apartment_type in APARTMENTS_DETAILS.keys():
            summary = {}
            amount = APARTMENTS_DETAILS[apartment_type]["amount_per_constructor"]
            size = APARTMENTS_DETAILS[apartment_type]["size"]
            aparment_cost_1 = size * C1 + land_cost
            aparment_cost_2 = size * C2 + land_cost
            total_construction_cost_1 += aparment_cost_1 * amount
            total_construction_cost_2 += aparment_cost_2 * amount

            price_without_tax_1 = aparment_cost_1 * (net_operational_profit + 1)
            price_with_tax_1 = (price_without_tax_1 - TAX_THRESHOLD) * TAX_PERCENTAGE + price_without_tax_1 \
              if price_without_tax_1 > TAX_THRESHOLD else price_without_tax_1
            price_without_tax_2 = aparment_cost_2 * (net_operational_profit + 1)
            price_with_tax_2 = (price_without_tax_2 - TAX_THRESHOLD) * TAX_PERCENTAGE + price_without_tax_2 \
                if price_without_tax_2 > TAX_THRESHOLD else price_without_tax_2

            apartment_1_profit = round(price_without_tax_1 - aparment_cost_1)
            apartment_2_profit = round(price_without_tax_2 - aparment_cost_2)

            summary["price_without_tax_1"] = price_without_tax_1
            summary["price_with_tax_1"] = price_with_tax_1
            summary["price_without_tax_2"] = price_without_tax_2
            summary["price_with_tax_2"] = price_with_tax_2
            summary["apartment_1_profit"] = apartment_1_profit
            summary["apartment_2_profit"] = apartment_2_profit

            # Subsidy calculations
            subsidized_price_relative_diff_2 = (price_with_tax_2 - price_with_tax_1 - subsidy_level) / price_with_tax_2
            # If the subsidy effect is not significant, the part of "green" demand will be set by the education effects.
            # Otherwise, we'll add to the demand the affected part.
            if subsidized_price_relative_diff_2 < MIN_PRICE_DIFF:
              u2_after_subsidy += SI * u3_post_education * (amount / MAX_CONSTRUCTOR_APARTMENTS)
            
            # Profit calculations
            h1 += apartment_1_profit * amount

            total_summary[apartment_type] = summary
          
          m2_after_subsidy = round(u2_after_subsidy * M) if constructor_index == 0 else last_residual_m2_subsidy
          quota_m2_subsidy = min(m2_after_subsidy, MAX_CONSTRUCTOR_APARTMENTS)
          merge_m2_subsidy = MAX_CONSTRUCTOR_APARTMENTS \
            if quota_m2_subsidy / MAX_CONSTRUCTOR_APARTMENTS >= CONSTRUCTOR_MOTIVATION_RATIO \
            else 0

          # Profit calculations
          h2 = (apartment_2_profit * merge_m2_subsidy) + (apartment_1_profit * (MAX_CONSTRUCTOR_APARTMENTS - merge_m2_subsidy))

          record = {
            "Iteration": iteration_number,
            "B Type": area,
            "Constructor": constructor_index + 1,
            "Land Cost": land_cost,
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
          last_residual_m2_subsidy = 0 if merge_m2_subsidy == 0 else (
              max(m2_after_subsidy - merge_m2_subsidy, 0)
            )

  return final_data_frame