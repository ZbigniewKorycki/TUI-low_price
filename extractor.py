import pandas as pd
import os


def start_extractor():
    if os.path.exists("Offers_under_1500_TUI.csv"):
        os.remove("Offers_under_1500_TUI.csv")

    offers = pd.read_csv(
        "TUI_last_minute_offers.csv", encoding="ISO-8859-2", encoding_errors="replace"
    )

    not_acceptable_ratings = ["2/5", "2.5/5", "3/5", "3.5/5"]
    not_acceptable_countries = ["Bułgaria", "Albania", "Węgry", "Czechy", "Austria"]
    not_acceptable_hotels = ["Savvas", "Marianna Apart Hotel"]

    offers_price_below_1500 = offers.loc[offers["price"] <= 5000]

    offers_with_rating_above_4_or_none = offers[
        ~offers["trip_advisor_rating"].isin(not_acceptable_ratings)
    ]
    offers_with_wished_countries = offers[~offers["country"].isin(not_acceptable_countries)]

    offers_above_4_wished_countries_below_1500 = pd.merge(
        pd.merge(
            offers_with_rating_above_4_or_none, offers_with_wished_countries, how="inner"
        ),
        offers_price_below_1500,
        how="inner",
    )

    final_offers_1500 = offers_above_4_wished_countries_below_1500[
        ~offers_above_4_wished_countries_below_1500["hotel"].isin(not_acceptable_hotels)
    ]

    if not final_offers_1500.empty:
        final_offers_1500.to_csv("Offers_under_1500_TUI.csv")
