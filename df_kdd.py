def calculate_region_average_apartment_price(df, region):
    total_prices = 0

    region_prices = df[df['Region'] == region]['LandPricePerUnit']
    for price in region_prices:
        total_prices += float(price.replace('₪', '').replace(',', ''))

    return round(total_prices / len(region_prices))
