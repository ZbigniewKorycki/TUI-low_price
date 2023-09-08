import pandas as pd

offers = pd.read_csv("TUI_last_minute_offers.csv", encoding='ISO-8859-2', encoding_errors='replace')

offers_price_below_1500 = offers.loc[offers['price'] <= 1500]
offers_price_below_1250 = offers.loc[offers['price'] <= 1250]
offers_price_below_1000 = offers.loc[offers['price'] <= 1000]

offers_with_rating_above_4_or_none = offers.loc[
    (pd.isna(offers['trip_advisor_rating'])) | (offers['trip_advisor_rating'] == '4.5/5') | (
                offers['trip_advisor_rating'] == '4/5')]

countries_offer_to_delete = ['Bułgaria', 'Albania', 'Węgry', 'Czechy', 'Austria']

offers_with_wished_countries = offers[~offers['country'].isin(countries_offer_to_delete)]

offers_above_4_wished_countries_below_1500 = pd.merge(
    pd.merge(offers_with_rating_above_4_or_none, offers_with_wished_countries, how='inner'), offers_price_below_1500,
    how="inner")
offers_above_4_wished_countries_below_1250 = pd.merge(
    pd.merge(offers_with_rating_above_4_or_none, offers_with_wished_countries, how='inner'), offers_price_below_1250,
    how="inner")
offers_above_4_wished_countries_below_1000 = pd.merge(
    pd.merge(offers_with_rating_above_4_or_none, offers_with_wished_countries, how='inner'), offers_price_below_1000,
    how="inner")

bad_hotels = ['Savvas', 'Marianna Apart Hotel']

final_offers_1500 = offers_above_4_wished_countries_below_1500[
    ~offers_above_4_wished_countries_below_1500['hotel'].isin(bad_hotels)]
final_offers_1250 = offers_above_4_wished_countries_below_1250[
    ~offers_above_4_wished_countries_below_1250['hotel'].isin(bad_hotels)]
final_offers_1000 = offers_above_4_wished_countries_below_1000[
    ~offers_above_4_wished_countries_below_1000['hotel'].isin(bad_hotels)]

if not final_offers_1500.empty:
    print(final_offers_1500)
if not final_offers_1250.empty:
    print(final_offers_1250)
if not final_offers_1000.empty:
    print(final_offers_1000)

# print(offers)
#
# print(offers_price_below_1500)
# print(offers_price_below_1200.empty)
# print(offers_price_below_1000.empty)
