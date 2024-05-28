##################
# Type of buyers #
##################
# Buyes motivated by price only (%)
U1 = 0.3
# Buyers motivated by quality only (%)
U2 = 0.025
# Buyers that under certain manipulation might change their decision (%)
U3 = 1 - (U1 + U2)

# ? (%)
OP = 0.2

####################
# Apartments count #
####################
# Total Apartments Quantity in the neighborhood
M = 2000
# 3 bedrooms apartment quantity (15% of total apartments)
A3_COUNT = M * 15/100
# 4 bedrooms apartment quantity (40% of total apartments)
A4_COUNT = M * 40/100
# 5 bedrooms apartment quantity (35% of total apartments)
A5_COUNT = M * 35/100
# 6 bedrooms apartment quantity (10% of total apartments)
A6_COUNT = M * 10/100


# Contractors Quantity in the neighborhood
N = 10

# Maximum Subsidy by government (NIS)
Smax = 25000

# Minimum Subsidy by government (NIS)
Smin = 0

# Subsidiary Influence on U2 parameter (%)
SI = 0.1

# Total government investment in marketing & education for green construction (NIS)
E = 3_000_000

# Education Factor
EI = 0.00005

###################
# Apartments size #
###################
# Standard 3 bedrooms apartment total size (sqm)
A3_SIZE = 88
# Standard 4 bedrooms apartment total size (sqm)
A4_SIZE = 118
# Standard 5 bedrooms apartment total size (sqm)
A5_SIZE = 147
# Standard 6 bedrooms apartment total size (sqm)
A6_SIZE = 176
	
# Competitive factor that effects every additional contractor that start to promote apartments in the tested neighborhood
CF = 0.005

##################
# Building costs #
##################
# Standard construction cost per SQM (NIS)
C1 = 7360
# Green construction cost per SQM (NIS)
C2 = C1 * 1.042