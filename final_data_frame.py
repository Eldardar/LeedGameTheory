import pandas as pd
import math

from constants import APARTMENTS_DETAILS, C1, C2, COMPETITIVE_FACTOR, CONSTRUCTOR_MOTIVATION_RATIO, CONTRACTORS_AMOUNT, DEMAND_AREAS_EDUCATIONAL_EFFECTS, E, EDUCATION_BUDGET_LEVELS, EDUCATION_LEVEL_COST_LEVELS, M, MAX_CONSTRUCTOR_APARTMENTS, MIN_PRICE_DIFF, OPERATIONAL_PROFIT_1, PROFIT_EXTRA_CHARGE_2, SI, DEMAND_AREAS, SUBSIDY_LIMIT_LEVEL, TAX_PERCENTAGE, TAX_THRESHOLD, U1, U2, U3
from utils import to_percentage_string

def find_education_cost_and_factor(education_budget):
  for education_cost in EDUCATION_LEVEL_COST_LEVELS:
    if education_cost <= education_budget:
      return education_cost, EDUCATION_LEVEL_COST_LEVELS[education_cost]
  
  return 0, 0

FIELDS = ["Iteration",
          "B Type",
          "Constructor",
          "Education Budget",
          "Subdsidy Budget",
          "Subsidy Level",
          "Education Spare Budget",
          "Subsidy Spare Budget",
          "Land Cost",
          "CC1",
          "CC2",
          "Net OP 1",
          "A3 P1",
          "A3 P2",
          "A3 Subsidy Level",
          "A4 P1",
          "A4 P2",
          "A4 Subsidy Level",
          "A5 P1",
          "A5 P2",
          "A5 Subsidy Level",
          "A6 P1",
          "A6 P2",
          "A6 Subsidy Level",
          "Education Cost",
          "Education affect",
          "EI",
          "U2-After-Education",
          "U3-After-Education",
          "Subsidy Level Cap",
          "Subsidy Left",
          "A3 Constructor Amount",
          "Green A3 Demand",
          "Green A3 Total Built",
          "Green A3 Percentage Built",
          "Green A3 Amount left",
          "A4 Constructor Amount",
          "Green A4 Demand",
          "Green A4 Total Built",
          "Green A4 Percentage Built",
          "Green A4 Amount left",
          "A5 Constructor Amount",
          "Green A5 Demand",
          "Green A5 Total Built",
          "Green A5 Percentage Built",
          "Green A5 Amount left",
          "A6 Constructor Amount",
          "Green A6 Demand",
          "Green A6 Total Built",
          "Green A6 Percentage Built",
          "Green A6 Amount left",
          "H1",
          "H2",
          "Total Green Apartments",
          "Constructor Profit"]

def genereate_final_data_frame(land_cost_averages):
  final_data_frame = pd.DataFrame(columns=FIELDS)
  iteration_number = 0
  last_residual_m2_subsidy = 0

  for education_budget_level in EDUCATION_BUDGET_LEVELS:
    education_budget = education_budget_level * E
    subsidy_budget = E * (1 - education_budget_level)

    # Education calculations
    # Find the highest level of education that the budget covers
    education_cost, education_factor_level = find_education_cost_and_factor(education_budget)
    
    # Calculate spare budget from education
    education_spare_budget = education_budget - education_cost

    for area in DEMAND_AREAS:
      iteration_number += 1
      
      # Education affect
      education_affect = education_factor_level * DEMAND_AREAS_EDUCATIONAL_EFFECTS[area]
      u2_after_education = U2 + education_affect
      u3_post_education = 1 - u2_after_education - U1

      # TODO1: Need to enter subsidy steps here (make more iterations)
      for subsidy_level in SUBSIDY_LIMIT_LEVEL[area]:
        # subsidy_level = SUBSIDY_LIMIT_LEVEL[area]
        subsidy_left = subsidy_budget
        type_2_total_constructed = 0
        apartments_type2_totals = {}

        for constructor_index in range(CONTRACTORS_AMOUNT):
          # Cost calculations
          land_cost = land_cost_averages[area]
          net_operational_profit_1 = OPERATIONAL_PROFIT_1 - (constructor_index * COMPETITIVE_FACTOR)
          # net_operational_profit_2 = OPERATIONAL_PROFIT_2 - (constructor_index * COMPETITIVE_FACTOR)

          total_construction_cost_1 = 0
          total_construction_cost_2 = 0
          u2_after_subsidy = u2_after_education
          h1 = 0
          h2 = 0
          total_constructor_profit = 0
          for apartment_type in APARTMENTS_DETAILS.keys():
            apartment_type_h1 = 0
            apartment_type_h2 = 0
            amount = APARTMENTS_DETAILS[apartment_type]["amount_per_constructor"]
            size = APARTMENTS_DETAILS[apartment_type]["size"]
            aparment_cost_1 = size * C1 + land_cost
            aparment_cost_2 = size * C2 + land_cost
            total_construction_cost_1 += aparment_cost_1 * amount
            total_construction_cost_2 += aparment_cost_2 * amount

            price_without_tax_1 = aparment_cost_1 * (net_operational_profit_1 + 1)
            price_with_tax_1 = (price_without_tax_1 - TAX_THRESHOLD) * TAX_PERCENTAGE + price_without_tax_1 \
              if price_without_tax_1 > TAX_THRESHOLD else price_without_tax_1
            # Constructor profit for type 2 apartments is 6%
            # price_without_tax_2 = aparment_cost_2 * (net_operational_profit_2 + 1)
            price_without_tax_2 = price_with_tax_1 * PROFIT_EXTRA_CHARGE_2
            price_with_tax_2 = (price_without_tax_2 - TAX_THRESHOLD) * TAX_PERCENTAGE + price_without_tax_2 \
                if price_without_tax_2 > TAX_THRESHOLD else price_without_tax_2

            apartment_1_profit = round(price_without_tax_1 - aparment_cost_1)
            apartment_2_profit = round(price_without_tax_2 - aparment_cost_2)

            # Subsidy calculations
            # Subsidy won't cover more than the gap between type 1 and type 2 apartments
            single_subsidy_cost = min(subsidy_level, price_with_tax_2 - price_with_tax_1)
            subsidized_price_relative_diff_2 = (price_with_tax_2 - price_with_tax_1 - single_subsidy_cost) / price_with_tax_2
            # If the subsidy effect is not significant, the part of "green" demand will be set by the education effects.
            # Otherwise, we'll add to the demand the affected part.
            if subsidized_price_relative_diff_2 <= MIN_PRICE_DIFF and subsidy_left > 0:
              subsidy_costs_for_highly_drived_demand = u2_after_education * amount * single_subsidy_cost 
              subsidy_left_for_subsidy_effects = subsidy_left - subsidy_costs_for_highly_drived_demand
              type_2_apartments_left_for_subsidy_effects = (SI * u3_post_education * amount) // subsidy_left_for_subsidy_effects

              u2_after_subsidy += type_2_apartments_left_for_subsidy_effects / MAX_CONSTRUCTOR_APARTMENTS
              area_type_2_apartments_demand_percentage = u2_after_subsidy
            else:
              area_type_2_apartments_demand_percentage = u2_after_education
              
            amount_left = amount * (CONTRACTORS_AMOUNT - constructor_index)

            if apartment_type not in apartments_type2_totals:
              apartments_type2_totals[apartment_type] = {}
              apartments_type2_totals[apartment_type]["demand"] = \
                math.floor(amount_left * area_type_2_apartments_demand_percentage)
              apartments_type2_totals[apartment_type]["constructed"] = 0

            type_2_constructor_offer_amount = min(
              apartments_type2_totals[apartment_type]["demand"] - apartments_type2_totals[apartment_type]["constructed"],
              amount
            )

            # Profit calculations
            apartment_type_h1 = apartment_1_profit * amount
            apartment_type_h2 = type_2_constructor_offer_amount * apartment_2_profit \
              + (amount - type_2_constructor_offer_amount) * apartment_1_profit
            
            h1 += apartment_type_h1
            h2 += apartment_type_h2

            # Construcotr choice
            if apartment_type_h2 >= apartment_type_h1:
              total_constructor_profit += apartment_type_h2
              type_2_total_constructed += type_2_constructor_offer_amount
              apartments_type2_totals[apartment_type]["constructed"] += type_2_constructor_offer_amount
              if subsidy_left > 0:
                subsidy_left -= type_2_constructor_offer_amount * single_subsidy_cost
            else:
              total_constructor_profit += apartment_type_h1

            # total_summary[apartment_type] = summary
            apartments_type2_totals[apartment_type]["P1"] = round(price_with_tax_1)
            apartments_type2_totals[apartment_type]["P2"] = round(price_with_tax_2)
            apartments_type2_totals[apartment_type]["subsidy_level"] = round(single_subsidy_cost)
          
          m2_after_subsidy = round(u2_after_subsidy * M) if constructor_index == 0 else last_residual_m2_subsidy
          quota_m2_subsidy = min(m2_after_subsidy, MAX_CONSTRUCTOR_APARTMENTS)
          merge_m2_subsidy = MAX_CONSTRUCTOR_APARTMENTS \
            if quota_m2_subsidy / MAX_CONSTRUCTOR_APARTMENTS >= CONSTRUCTOR_MOTIVATION_RATIO \
            else 0

          record = {
            "Iteration": iteration_number,
            "B Type": area,
            "Constructor": constructor_index + 1,
            "Education Budget": education_budget,
            "Subdsidy Budget": subsidy_budget,
            "Subsidy Level": subsidy_level,
            "Education Spare Budget": education_spare_budget,
            "Subsidy Spare Budget": subsidy_left,
            "Land Cost": land_cost,
            "CC1": round(total_construction_cost_1),
            "CC2": round(total_construction_cost_2),
            "Net OP 1": to_percentage_string(net_operational_profit_1),
            "A3 P1": apartments_type2_totals["A3"]["P1"],
            "A3 P2": apartments_type2_totals["A3"]["P2"],
            "A3 Subsidy Level": apartments_type2_totals["A3"]["subsidy_level"],
            "A4 P1": apartments_type2_totals["A4"]["P1"],
            "A4 P2": apartments_type2_totals["A4"]["P2"],
            "A4 Subsidy Level": apartments_type2_totals["A4"]["subsidy_level"],
            "A5 P1": apartments_type2_totals["A5"]["P1"],
            "A5 P2": apartments_type2_totals["A5"]["P2"],
            "A5 Subsidy Level": apartments_type2_totals["A5"]["subsidy_level"],
            "A6 P1": apartments_type2_totals["A6"]["P1"],
            "A6 P2": apartments_type2_totals["A6"]["P2"],
            "A6 Subsidy Level": apartments_type2_totals["A6"]["subsidy_level"],
            "Education Cost": education_cost,
            "Education affect": education_affect,
            "U2-After-Education": to_percentage_string(u2_after_education),
            "U3-After-Education": to_percentage_string(u3_post_education),
            "Subsidy Level Cap": subsidy_level,
            "Subsidy Left": subsidy_left,
            "A3 Constructor Amount": APARTMENTS_DETAILS["A3"]["amount_per_constructor"],
            "Green A3 Demand": apartments_type2_totals["A3"]["demand"],
            "Green A3 Total Built": apartments_type2_totals["A3"]["constructed"],
            "Green A3 Percentage Built": to_percentage_string(apartments_type2_totals["A3"]["constructed"] / (APARTMENTS_DETAILS["A3"]["amount_per_constructor"] * CONTRACTORS_AMOUNT)),
            "Green A3 Amount left": apartments_type2_totals["A3"]["demand"] - apartments_type2_totals["A3"]["constructed"],
            "A4 Constructor Amount": APARTMENTS_DETAILS["A4"]["amount_per_constructor"],
            "Green A4 Demand": apartments_type2_totals["A4"]["demand"],
            "Green A4 Total Built": apartments_type2_totals["A4"]["constructed"],
            "Green A4 Percentage Built": to_percentage_string(apartments_type2_totals["A4"]["constructed"] / (APARTMENTS_DETAILS["A4"]["amount_per_constructor"] * CONTRACTORS_AMOUNT)),
            "Green A4 Amount left": apartments_type2_totals["A4"]["demand"] - apartments_type2_totals["A4"]["constructed"],
            "A5 Constructor Amount": APARTMENTS_DETAILS["A5"]["amount_per_constructor"],
            "Green A5 Demand": apartments_type2_totals["A5"]["demand"],
            "Green A5 Total Built": apartments_type2_totals["A5"]["constructed"],
            "Green A5 Percentage Built": to_percentage_string(apartments_type2_totals["A5"]["constructed"] / (APARTMENTS_DETAILS["A5"]["amount_per_constructor"] * CONTRACTORS_AMOUNT)),
            "Green A5 Amount left": apartments_type2_totals["A5"]["demand"] - apartments_type2_totals["A5"]["constructed"],
            "A6 Constructor Amount": APARTMENTS_DETAILS["A6"]["amount_per_constructor"],
            "Green A6 Demand": apartments_type2_totals["A6"]["demand"],
            "Green A6 Total Built": apartments_type2_totals["A6"]["constructed"],
            "Green A6 Percentage Built": to_percentage_string(apartments_type2_totals["A6"]["constructed"] / (APARTMENTS_DETAILS["A6"]["amount_per_constructor"] * CONTRACTORS_AMOUNT)),
            "Green A6 Amount left": apartments_type2_totals["A6"]["demand"] - apartments_type2_totals["A6"]["constructed"],
            "H1": h1,
            "H2": h2,
            "Total Green Apartments": type_2_total_constructed,
            "Constructor Profit": total_constructor_profit,
          }
          
          # TODO: Create a list of records and then put it under a dataframe
          new_record_data_frame = pd.DataFrame([record])
          final_data_frame = pd.concat([final_data_frame, new_record_data_frame], ignore_index=True)

          # Data for next iteration
          last_residual_m2_subsidy = 0 if merge_m2_subsidy == 0 else (
              max(m2_after_subsidy - merge_m2_subsidy, 0)
            )

  return final_data_frame