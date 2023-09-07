from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time


def init_driver(link_to_scrape):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 3)
    driver.get(link_to_scrape)
    driver.maximize_window()
    accept_cookies_button = driver.find_element(By.XPATH, "//button[contains(., 'Zaakceptuj')]")
    accept_cookies_button.click()
    time.sleep(1)
    original_window = driver.window_handles[0]
    last_minute_offers_button = driver.find_elements(By.CLASS_NAME, "desktop-menu-nav__link")[0]
    last_minute_offers_button.click()
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    time.sleep(3)
    # choosing list of airport from where last minute offers should be shown
    dropdown_airports_of_departure = driver.find_element(By.CSS_SELECTOR,
                                                         'button[data-testid="dropdown-field--airport"]')
    dropdown_airports_of_departure.click()
    time.sleep(1)
    airports = driver.find_elements(By.CLASS_NAME, "bp3-control-indicator")[10]
    airports.click()
    dropdown_airports_of_departure_submit = driver.find_element(By.CSS_SELECTOR,
                                                                'button[data-testid="dropdown-window-button-submit"]')
    dropdown_airports_of_departure_submit.click()
    time.sleep(3)
    # choosing date period of arrivals

    date_range_to_find_offers_start = 15

    while date_range_to_find_offers_start < 23:

        dropdown_dates = driver.find_element(By.CSS_SELECTOR,
                                             'button[data-testid="dropdown-field--travel-date"]')
        dropdown_dates.click()
        time.sleep(1)
        specific_day_offers = driver.find_element(By.CSS_SELECTOR,
                                             'div[data-tab-id="tab-gs-travelDate-single"]')
        specific_day_offers.click()
        time.sleep(1)
        offers_arrivals_from_date = driver.find_element(By.CSS_SELECTOR, f'time[datetime="2023-09-{date_range_to_find_offers_start}T00:00:00.000"]')
        offers_arrivals_from_date.click()
        time.sleep(1)
        dropdown_date_period_arrivals_submit = driver.find_element(By.CSS_SELECTOR,
                                                                   'button[data-testid="dropdown-window-button-submit"]')
        dropdown_date_period_arrivals_submit.click()

        time.sleep(2)

        global_search_button_submit = driver.find_element(By.CSS_SELECTOR,
                                                          'button[data-testid="global-search-button-submit"]')
        global_search_button_submit.click()
        time.sleep(10)
        offers = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="offer-tile"]')

        for offer in offers:
            try:
                hotel = offer.find_element(By.CLASS_NAME, 'offer-tile-body__header').text
            except NoSuchElementException:
                hotel = None
            try:
                country = offer.find_element(By.XPATH, f'//a[@hotelname="{hotel}"]').get_attribute('destination').split(", ")[0]
            except NoSuchElementException:
                country = None
            try:
                region = offer.find_element(By.XPATH, f'//a[@hotelname="{hotel}"]').get_attribute('destination').split(", ")[1:]
            except NoSuchElementException:
                region = None
            try:
                offer_link = offer.find_element(By.XPATH, f'//a[@hotelname="{hotel}"]').get_attribute('href')
            except NoSuchElementException:
                offer_link = None
            try:
                trip_advisor_rating = offer.find_element(By.CSS_SELECTOR, 'div[data-testid="tripadvisor-opinions-badge"]').text.split("\n")[0]
            except NoSuchElementException:
                trip_advisor_rating = None
            try:
                trip_advisor_opinions = offer.find_element(By.CSS_SELECTOR, 'div[data-testid="tripadvisor-opinions-badge"]').text.split("\n")[1]
            except NoSuchElementException:
                trip_advisor_opinions = None
            try:
                departure_airport = offer.find_element(By.CSS_SELECTOR, 'div[data-testid="dropdown--same-day-offers"]').text.split(" ")[0]
            except NoSuchElementException:
                departure_airport = None
            try:
                departure_time = offer.find_element(By.CSS_SELECTOR, 'div[data-testid="dropdown--same-day-offers"]').text.split(" ")[1].replace("(", "").replace(")", "")
            except NoSuchElementException:
                departure_time = None
            try:
                price = offer.find_element(By.CSS_SELECTOR, 'span[data-testid="price-amount"]').text.replace(" ", "")
            except NoSuchElementException:
                price = None
            try:
                currency = offer.find_element(By.CLASS_NAME, 'price-value__currency').text
            except NoSuchElementException:
                currency = None
            try:
                board_type = offer.find_element(By.CSS_SELECTOR, 'span[data-testid="offer-tile-boardType"]').text
            except NoSuchElementException:
                board_type = None
            try:
                offer_dates = offer.find_element(By.CSS_SELECTOR, 'span[data-testid="offer-tile-departure-date"]').text
            except NoSuchElementException:
                offer_dates = None
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
            print(f"offer_dates: {offer_dates}")
            print(f"offer_link: {offer_link}")
        date_range_to_find_offers_start += 1
        time.sleep(5)
    driver.quit()


init_driver("https://www.tui.pl/")
