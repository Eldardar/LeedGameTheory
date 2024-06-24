def calculate_region_average_apartment_price(df, region):
    total_prices = 0

    region_weighed_prices = df[df['Region'] == region][['LandPricePerUnit','NumberOfUnits']].copy()
    total_weights = region_weighed_prices['NumberOfUnits'] \
        .map(lambda x: int(x.replace(',', ''))) \
        .sum()

    for i in range(len(region_weighed_prices)):
        region_details = region_weighed_prices.iloc[i]

        region_price = float(region_details['LandPricePerUnit'].replace('₪', '').replace(',', ''))
        region_weight = int(region_details['NumberOfUnits'].replace(',', ''))
        total_prices += region_price * region_weight

    return round(total_prices / total_weights)
