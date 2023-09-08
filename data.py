import pandas as pd

data = pd.read_csv("TUI_last_minute_offers.csv", encoding='utf-8', encoding_errors='replace')

offers_price_below_1500 = data.loc[data['price'] <= 1500]
offers_price_below_1200 = data.loc[data['price'] <= 1200]
offers_price_below_1000 = data.loc[data['price'] <= 1000]



print(offers_price_below_1500.empty)
print(offers_price_below_1200.empty)
print(offers_price_below_1000.empty)
