import pandas as pd

offers = pd.read_csv("TUI_last_minute_offers.csv", encoding='ISO-8859-2', encoding_errors='replace')

offers_price_below_1500 = offers.loc[offers['price'] <= 1500]
offers_price_below_1200 = offers.loc[offers['price'] <= 1250]
offers_price_below_1000 = offers.loc[offers['price'] <= 1000]

print(offers)

print(offers_price_below_1500.empty)
print(offers_price_below_1200.empty)
print(offers_price_below_1000.empty)
