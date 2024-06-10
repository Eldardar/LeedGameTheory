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
APARTMENT_TYPES = ["A3", "A4", "A5", "A6"]
# Total Apartments Quantity in the neighborhood
M = 2000
# Apartments quantity (% of total apartments)
APARTMENTS_COUNT = {
    "A3": M * 15 / 100,
    "A4": M * 40 / 100,
    "A5": M * 35 / 100,
    "A6": M * 10 / 100,
}
# Apartments total size (sqm)
APARTMENTS_SIZE = {
    "A3": 88,
    "A4": 118,
    "A5": 147,
    "A6": 176,
}
# Base demand for "green" building
M2_BASE = 50

###########################
# Construction properties #
###########################
# Standard construction cost per SQM (NIS)
C1 = 7360
# Green construction cost per SQM (NIS)
C2 = C1 * 1.042
# Contractors Quantity in the neighborhood
CONTRACTORS_AMOUNT = 10
# Max apartments per constructor
MAX_CONSTRUCTOR_APARTMENTS = 200
# When half of the apartments are expensive, the constructor will build only
# expensive apartments.
# Otherwise, the constructor will build only cheap apartments. (%)
CONSTRUCTOR_MOTIVATION_RATIO = 50 / 100
# Operational profit for each contractor (%)
OPERATIONAL_PROFIT = 20 / 100
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
# Total government investment in marketing & education for green
# construction (NIS)
E = 3_000_000
# Goverment's investment in education (millions NIS)
EDUCATION_INVESTMENT_LEVELS = list(range(16))
# Education impact factor (%)
EI = 0.005 / 100