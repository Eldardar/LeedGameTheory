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
OPERATIONAL_PROFIT = 15 / 100
# Competitive factor that effects every additional contractor
# that start to promote apartments in the tested neighborhood (%)
COMPETITIVE_FACTOR = 0.5 / 100

##################
# TAX properties #
##################
TAX_THRESHOLD = 1_919_155
TAX_PERCENTAGE = 3.5 / 100

######################
# Subsidy properties #
######################
SUBSIDY_LEVELS = [0, 5000, 10000, 15000, 20000, 25000]
# Subsidiary Influence on U2 parameter (%)
SI = 10 / 100
# Minimum Price Difference for Effect
MIN_PRICE_DIFF = 1.5 / 100

########################
# Education properties #
########################
EDUCATION_LEVEL_COST = 1_000_000
# Goverment's investment in education (millions NIS)
EDUCATION_LEVELS_COUNT = 16
# Education impact factor (%)
EI = 0.005 / 100

######################
# General properties #
######################
# Total government investment in marketing & education for green
# construction (NIS)
E = 15_000_000
GOVERNMENT_ACTIONS = {
  "Subsidy": len(SUBSIDY_LEVELS),
  "Education": EDUCATION_LEVELS_COUNT,
}