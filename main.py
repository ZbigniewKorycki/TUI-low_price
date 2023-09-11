import csv
import os
import time
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from extractor import start_extractor
from sender import start_sender


all_offers_from_given_dates = []


def find_element_with_exception(
    offer, by, selector, *, attribute=None, text_to_extract=False
):
    try:
        if attribute:
            element = offer.find_element(by, selector).get_attribute(attribute)
        else:
            element = offer.find_element(by, selector)
        if text_to_extract:
            return element.text
        else:
            return element
    except NoSuchElementException:
        return None


def process_variable(variable, operation=None, *args):
    if variable is not None:
        if operation:
            variable = operation(variable, *args)
        return variable
    return None


# operation functions
def split_and_get_first(text, delimiter):
    return text.split(delimiter)[0]


def split_and_get_second(text, delimiter):
    return text.split(delimiter)[1]


def remove_whitespace(text):
    return text.replace(" ", "")


def init_driver(link_to_scrape):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link_to_scrape)
    driver.maximize_window()
    accept_cookies_button = driver.find_element(
        By.XPATH, "//button[contains(., 'Zaakceptuj')]"
    )
    accept_cookies_button.click()
    time.sleep(1)
    last_minute_offers_button = driver.find_elements(
        By.CLASS_NAME, "desktop-menu-nav__link"
    )[0]
    last_minute_offers_button.click()
    window_after = driver.window_handles[1]
    time.sleep(3)
    driver.close()
    driver.switch_to.window(window_after)
    time.sleep(3)

    # choosing list of airport from where last minute offers should be shown
    try:
        dropdown_airports_of_departure = driver.find_element(
            By.CSS_SELECTOR, 'button[data-testid="dropdown-field--airport"]'
        )
        dropdown_airports_of_departure.click()
    except NoSuchElementException:
        time.sleep(1)
    else:
        time.sleep(1)
        acceptable_airports = ["Warszawa-Chopina", "Warszawa-Radom", "Warszawa-Modlin"]
        for airport in acceptable_airports:
            try:
                airport_checkbox = driver.find_element(
                    By.XPATH, f'//label[contains(text(), "{airport}")]'
                )
                airport_checkbox.click()
            except ElementClickInterceptedException:
                continue

        acceptable_airports_submit = driver.find_element(
            By.CSS_SELECTOR, 'button[data-testid="dropdown-window-button-submit"]'
        )
        acceptable_airports_submit.click()

    # choosing date period of arrivals
    time.sleep(1)
    start = datetime.now().strftime("%Y-%m-%d")
    num_of_dates = 2
    date_list = [
        datetime.strptime(start, "%Y-%m-%d").date() + timedelta(days=x)
        for x in range(num_of_dates)
    ]
    date_list_format_of_tui = [date.strftime("%Y-%m-%d") for date in date_list]
    for date in date_list_format_of_tui:
        try:
            dropdown_dates = driver.find_element(
                By.CSS_SELECTOR, 'button[data-testid="dropdown-field--travel-date"]'
            )
            dropdown_dates.click()
        except ElementClickInterceptedException:
            time.sleep(3)
            dropdown_dates = driver.find_element(
                By.CSS_SELECTOR, 'button[data-testid="dropdown-field--travel-date"]'
            )
            dropdown_dates.click()
        time.sleep(1)
        specific_day_offers = driver.find_element(
            By.CSS_SELECTOR, 'div[data-tab-id="tab-gs-travelDate-single"]'
        )
        specific_day_offers.click()
        time.sleep(1)
        offers_arrivals_from_date = driver.find_element(
            By.CSS_SELECTOR, f'time[datetime="{date}T00:00:00.000"]'
        )
        offers_arrivals_from_date.click()
        time.sleep(1)
        dropdown_date_period_arrivals_submit = driver.find_element(
            By.CSS_SELECTOR, 'button[data-testid="dropdown-window-button-submit"]'
        )
        dropdown_date_period_arrivals_submit.click()
        time.sleep(3)
        try:
            global_search_button_submit = driver.find_element(
                By.CSS_SELECTOR, 'button[data-testid="global-search-button-submit"]'
            )
            global_search_button_submit.click()
        except ElementClickInterceptedException:
            time.sleep(5)
            global_search_button_submit = driver.find_element(
                By.CSS_SELECTOR, 'button[data-testid="global-search-button-submit"]'
            )
            global_search_button_submit.click()

        time.sleep(15)
        offers_for_current_day = driver.find_elements(
            By.CSS_SELECTOR, 'div[data-testid="offer-tile"]'
        )
        for offer in offers_for_current_day:
            hotel = find_element_with_exception(
                offer, By.CLASS_NAME, "offer-tile-body__header", text_to_extract=True
            )
            country = find_element_with_exception(
                offer, By.XPATH, f'//a[@hotelname="{hotel}"]', attribute="destination"
            )
            region = find_element_with_exception(
                offer, By.XPATH, f'//a[@hotelname="{hotel}"]', attribute="destination"
            )
            offer_link = find_element_with_exception(
                offer, By.XPATH, f'//a[@hotelname="{hotel}"]', attribute="href"
            )
            trip_advisor_rating = find_element_with_exception(
                offer,
                By.CSS_SELECTOR,
                'div[data-testid="tripadvisor-opinions-badge"]',
                text_to_extract=True,
            )
            trip_advisor_opinions = find_element_with_exception(
                offer,
                By.CSS_SELECTOR,
                'div[data-testid="tripadvisor-opinions-badge"]',
                text_to_extract=True,
            )
            trip_advisor_opinions = process_variable(
                trip_advisor_opinions, split_and_get_second, "\n"
            )
            departure_airport = find_element_with_exception(
                offer,
                By.CSS_SELECTOR,
                'div[data-testid="dropdown--same-day-offers"]',
                text_to_extract=True,
            )
            departure_time = find_element_with_exception(
                offer,
                By.CSS_SELECTOR,
                'div[data-testid="dropdown--same-day-offers"]',
                text_to_extract=True,
            )

            price = find_element_with_exception(
                offer,
                By.CSS_SELECTOR,
                'span[data-testid="price-amount"]',
                text_to_extract=True,
            )
            currency = find_element_with_exception(
                offer, By.CLASS_NAME, "price-value__currency", text_to_extract=True
            )
            board_type = find_element_with_exception(
                offer,
                By.CSS_SELECTOR,
                'span[data-testid="offer-tile-boardType"]',
                text_to_extract=True,
            )
            offer_date = find_element_with_exception(
                offer,
                By.CSS_SELECTOR,
                'span[data-testid="offer-tile-departure-date"]',
                text_to_extract=True,
            )

            country = process_variable(country, split_and_get_first, ", ")
            trip_advisor_rating = process_variable(
                trip_advisor_rating, split_and_get_first, "\n"
            )
            departure_airport = process_variable(
                departure_airport, split_and_get_first, " "
            )
            departure_time = process_variable(departure_time, split_and_get_second, " ")
            price = process_variable(price, remove_whitespace)

            single_offer = {
                "hotel": hotel,
                "country": country,
                "region": region,
                "trip_advisor_rating": trip_advisor_rating,
                "trip_advisor_opinions": trip_advisor_opinions,
                "departure_airport": departure_airport,
                "departure_time": departure_time,
                "price": price,
                "currency": currency,
                "board_type": board_type,
                "offer_date": offer_date,
                "offer_link": offer_link,
            }
            all_offers_from_given_dates.append(single_offer)
        time.sleep(5)
    if os.path.exists("TUI_last_minute_offers.csv"):
        os.remove("TUI_last_minute_offers.csv")
    tui_offers = "TUI_last_minute_offers.csv"
    fields = [
        "hotel",
        "country",
        "region",
        "offer_link",
        "trip_advisor_rating",
        "trip_advisor_opinions",
        "departure_airport",
        "departure_time",
        "price",
        "currency",
        "board_type",
        "offer_date",
    ]
    with open(tui_offers, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_offers_from_given_dates)
    driver.quit()


init_driver("https://www.tui.pl/")
start_extractor()
start_sender()
