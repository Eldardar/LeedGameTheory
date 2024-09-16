DEMAND_AREAS = ["B1", "B2", "B3", "B4", "B5", "B6", "B7"]

##################
# Type of buyers #
##################
# Buyes motivated by price only (%)
U1 = 30 / 100
# Buyers motivated by quality only (%)
U2 = 2.5 / 100
# Buyers that under certain manipulation might change their decision (%)
U3 = 1 - (U1 + U2)

#########################
# Apartments properties #
#########################
# Total apartments in the neighborhood
M = 2000
# Max apartments per constructor (marked as W)
MAX_CONSTRUCTOR_APARTMENTS = 200
# Apartments details (distribution and size [sqm])
APARTMENTS_DETAILS = {
    "A3": {
      "amount_per_constructor": MAX_CONSTRUCTOR_APARTMENTS * 25 / 100,
      "size": 88,
    },
    "A4": {
      "amount_per_constructor": MAX_CONSTRUCTOR_APARTMENTS * 40 / 100,
      "size": 118,
    },
    "A5": {
      "amount_per_constructor": MAX_CONSTRUCTOR_APARTMENTS * 25 / 100,
      "size": 147,
    },
    "A6": {
      "amount_per_constructor": MAX_CONSTRUCTOR_APARTMENTS * 10 / 100,
      "size": 176,
    },
}
# Base demand for "green" building
M2_BASE = 50

###########################
# Construction properties #
###########################
# Standard construction cost per SQM (NIS)
C1 = 5602
# Green construction cost per SQM (NIS)
C2 = C1 * 1.07
# Contractors Quantity in the neighborhood
CONTRACTORS_AMOUNT = 10
# When half of the apartments are expensive, the constructor will build only
# expensive apartments.
# Otherwise, the constructor will build only cheap apartments. (%)
CONSTRUCTOR_MOTIVATION_RATIO = 50 / 100
# Operational profit for each contractor (%)
OPERATIONAL_PROFIT_1 = 15 / 100
# OPERATIONAL_PROFIT_2 = 14 / 100
PROFIT_EXTRA_CHARGE_2 = 106 / 100
# Competitive factor that effects every additional contractor
# that start to promote apartments in the tested neighborhood (%)
COMPETITIVE_FACTOR = 0.25 / 100

##################
# TAX properties #
##################
TAX_THRESHOLD = 1_919_155
TAX_PERCENTAGE = 3.5 / 100

######################
# Subsidy properties #
######################
# Subsidiary Influence on U2 parameter (%)
SI = 10 / 100
# Minimum Price Difference for Effect
MIN_PRICE_DIFF = 1.5 / 100
# Subsidy limit level
SUBSIDY_LIMIT_LEVEL = {
  "B1": [50_000, 100_000, 150_000],
  "B2": [50_000, 100_000, 150_000],
  "B3": [50_000, 100_000],
  "B4": [50_000, 100_000],
  "B5": [50_000],
  "B6": [50_000],
  "B7": [50_000],
}
SUBSIDY_LEVEL_STEP = 50_000

########################
# Education properties #
########################
# Education budget out of the total budget (%)
EDUCATION_BUDGET_LEVELS = [0/100, 25/100, 50/100, 75/100, 100/100]
# IMPORTANT - sort it from highest to lowest level
EDUCATION_LEVEL_COST_LEVELS = {
  15_000_000: 0.0977,
  11_500_000: 0.0881,
  8_000_000: 0.0562,
  4_500_000: 0.0182,
  1_000_000: 0.0037,
}
# Demand areas and their educational effects
DEMAND_AREAS_EDUCATIONAL_EFFECTS = {
  "B1": 100 / 100,
  "B2": 90 / 100,
  "B3": 80 / 100,
  "B4": 70 / 100,
  "B5": 60 / 100,
  "B6": 50 / 100,
  "B7": 50 / 100,
}

######################
# General properties #
######################
# Total government investment in marketing & education for green
# construction (NIS)
E = 15_000_000