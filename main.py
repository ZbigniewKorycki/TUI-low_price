from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
from datetime import datetime, timedelta
import csv

all_offers_from_given_dates = []


def find_element_with_exception(offer, by, selector, *, attribute=None, text_to_extract=False):
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


def init_driver(link_to_scrape):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 3)
    driver.get(link_to_scrape)
    driver.maximize_window()
    accept_cookies_button = driver.find_element(By.XPATH, "//button[contains(., 'Zaakceptuj')]")
    accept_cookies_button.click()
    time.sleep(1)
    last_minute_offers_button = driver.find_elements(By.CLASS_NAME, "desktop-menu-nav__link")[0]
    last_minute_offers_button.click()
    window_after = driver.window_handles[1]
    time.sleep(3)
    driver.close()
    driver.switch_to.window(window_after)
    time.sleep(3)

    # choosing list of airport from where last minute offers should be shown
    dropdown_airports_of_departure = driver.find_element(By.CSS_SELECTOR,
                                                         'button[data-testid="dropdown-field--airport"]')
    dropdown_airports_of_departure.click()

    time.sleep(1)
    acceptable_airports = ["Warszawa-Chopina", "Warszawa-Radom", "Warszawa-Modlin"]
    for airport in acceptable_airports:
        try:
            airport_checkbox = driver.find_element(By.XPATH, f'//label[contains(text(), "{airport}")]')
            airport_checkbox.click()
        except ElementClickInterceptedException:
            continue

    acceptable_airports_submit = driver.find_element(By.CSS_SELECTOR,
                                                     'button[data-testid="dropdown-window-button-submit"]')
    acceptable_airports_submit.click()
    time.sleep(3)

    # choosing date period of arrivals
    start = '2023-09-15'
    num_of_dates = 8
    date_list = [datetime.strptime(start, '%Y-%m-%d').date() + timedelta(days=x) for x in range(num_of_dates)]
    date_list_format_of_tui = [date.strftime("%Y-%m-%d") for date in date_list]
    for date in date_list_format_of_tui:
        dropdown_dates = driver.find_element(By.CSS_SELECTOR,
                                             'button[data-testid="dropdown-field--travel-date"]')
        dropdown_dates.click()
        time.sleep(1)
        specific_day_offers = driver.find_element(By.CSS_SELECTOR,
                                                  'div[data-tab-id="tab-gs-travelDate-single"]')
        specific_day_offers.click()
        time.sleep(1)
        offers_arrivals_from_date = driver.find_element(By.CSS_SELECTOR,
                                                        f'time[datetime="{date}T00:00:00.000"]')
        offers_arrivals_from_date.click()
        time.sleep(1)
        dropdown_date_period_arrivals_submit = driver.find_element(By.CSS_SELECTOR,
                                                                   'button[data-testid="dropdown-window-button-submit"]')
        dropdown_date_period_arrivals_submit.click()
        time.sleep(1)
        global_search_button_submit = driver.find_element(By.CSS_SELECTOR,
                                                          'button[data-testid="global-search-button-submit"]')
        global_search_button_submit.click()

        time.sleep(15)
        offers_for_current_day = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="offer-tile"]')
        for offer in offers_for_current_day:
            hotel = find_element_with_exception(offer, By.CLASS_NAME, 'offer-tile-body__header', text_to_extract=True)
            country = find_element_with_exception(offer, By.XPATH, f'//a[@hotelname="{hotel}"]',
                                                  attribute="destination")
            country = country.split(", ")[0]
            region = find_element_with_exception(offer, By.XPATH, f'//a[@hotelname="{hotel}"]', attribute="destination")
            offer_link = find_element_with_exception(offer, By.XPATH, f'//a[@hotelname="{hotel}"]', attribute="href")
            trip_advisor_rating = find_element_with_exception(offer, By.CSS_SELECTOR,
                                                              'div[data-testid="tripadvisor-opinions-badge"]',
                                                              text_to_extract=True)
            trip_advisor_rating = trip_advisor_rating.split("\n")[0]
            trip_advisor_opinions = find_element_with_exception(offer, By.CSS_SELECTOR,
                                                                'div[data-testid="tripadvisor-opinions-badge"]',
                                                                text_to_extract=True)
            trip_advisor_opinions = trip_advisor_opinions.split("\n")[1]
            departure_airport = find_element_with_exception(offer, By.CSS_SELECTOR,
                                                            'div[data-testid="dropdown--same-day-offers"]', text_to_extract=True)
            departure_airport = departure_airport.split(" ")[0]
            departure_time = find_element_with_exception(offer, By.CSS_SELECTOR,
                                                         'div[data-testid="dropdown--same-day-offers"]', text_to_extract=True)
            departure_time = departure_time.split(" ")[1].replace("(", "").replace(")", "")
            price = find_element_with_exception(offer, By.CSS_SELECTOR, 'span[data-testid="price-amount"]', text_to_extract=True)
            price = price.replace(" ", "")
            currency = find_element_with_exception(offer, By.CLASS_NAME, 'price-value__currency', text_to_extract=True)
            board_type = find_element_with_exception(offer, By.CSS_SELECTOR, 'span[data-testid="offer-tile-boardType"]',
                                                     text_to_extract=True)
            offer_date = find_element_with_exception(offer, By.CSS_SELECTOR,
                                                     'span[data-testid="offer-tile-departure-date"]', text_to_extract=True)

            print(f"Hotel: {hotel}")
            print(f"country: {country}")
            print(f"region : {region}")
            print(f"trip_advisor_rating: {trip_advisor_rating}")
            print(f"trip_advisor_opinions: {trip_advisor_opinions}")
            print(f"departure_airport: {departure_airport}")
            print(f"departure_time: {departure_time}")
            print(f"price: {price}")
            print(f"currency: {currency}")
            print(f"board_type: {board_type}")
            print(f"offer_date: {offer_date}")
            print(f"offer_link: {offer_link}")

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
                "offer_link": offer_link
            }
            all_offers_from_given_dates.append(single_offer)
        time.sleep(5)
    tui_offers = f"tui_offers_from_day_to.csv"
    fields = ["hotel", "country", "region", "offer_link", "trip_advisor_rating", "trip_advisor_opinions",
              "departure_airport", "departure_time", "price", "currency", "board_type", "offer_date"]
    with open(tui_offers, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_offers_from_given_dates)
    driver.quit()


init_driver("https://www.tui.pl/")

# for offer in offers_for_current_day:
#     try:
#         hotel = offer.find_element(By.CLASS_NAME, 'offer-tile-body__header')
#         hotel = hotel.text
#     except NoSuchElementException:
#         hotel = None
#     try:
#         country = offer.find_element(By.XPATH, f'//a[@hotelname="{hotel}"]')
#         country = country.get_attribute('destination').split(", ")[0]
#     except NoSuchElementException:
#         country = None
#     try:
#         region = offer.find_element(By.XPATH, f'//a[@hotelname="{hotel}"]')
#         region = region.get_attribute('destination')
#     except NoSuchElementException:
#         region = None
#     try:
#         offer_link = offer.find_element(By.XPATH, f'//a[@hotelname="{hotel}"]')
#         offer_link = offer_link.get_attribute('href')
#     except NoSuchElementException:
#         offer_link = None
#     try:
#         trip_advisor_rating = offer.find_element(By.CSS_SELECTOR,
#                                                  'div[data-testid="tripadvisor-opinions-badge"]')
#         trip_advisor_rating = trip_advisor_rating.text.split("\n")[0]
#     except NoSuchElementException:
#         trip_advisor_rating = None
#     try:
#         trip_advisor_opinions = offer.find_element(By.CSS_SELECTOR,
#                                                    'div[data-testid="tripadvisor-opinions-badge"]')
#         trip_advisor_opinions = trip_advisor_opinions.text.split("\n")[1]
#     except NoSuchElementException:
#         trip_advisor_opinions = None
#     try:
#         departure_airport = offer.find_element(By.CSS_SELECTOR, 'div[data-testid="dropdown--same-day-offers"]')
#         departure_airport = departure_airport.text.split(" ")[0]
#     except NoSuchElementException:
#         departure_airport = None
#     try:
#         departure_time = offer.find_element(By.CSS_SELECTOR, 'div[data-testid="dropdown--same-day-offers"]')
#         departure_time = departure_time.text.split(" ")[1].replace("(", "").replace(")", "")
#     except NoSuchElementException:
#         departure_time = None
#     try:
#         price = offer.find_element(By.CSS_SELECTOR, 'span[data-testid="price-amount"]')
#         price = price.text.replace(" ", "")
#     except NoSuchElementException:
#         price = None
#     try:
#         currency = offer.find_element(By.CLASS_NAME, 'price-value__currency')
#         currency = currency.text
#     except NoSuchElementException:
#         currency = None
#     try:
#         board_type = offer.find_element(By.CSS_SELECTOR, 'span[data-testid="offer-tile-boardType"]')
#         board_type = board_type.text
#     except NoSuchElementException:
#         board_type = None
#     try:
#         offer_date = offer.find_element(By.CSS_SELECTOR, 'span[data-testid="offer-tile-departure-date"]')
#         offer_date = offer_date.text
#     except NoSuchElementException:
#         offer_date = None
