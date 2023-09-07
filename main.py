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
    #choosing list of airport from where last minute offers should be shown
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
    #choosing date period of arrivals
    dropdown_dates = driver.find_element(By.CSS_SELECTOR,
                                                         'button[data-testid="dropdown-field--travel-date"]')
    dropdown_dates.click()
    time.sleep(1)
    offers_arrivals_from_date = driver.find_element(By.CSS_SELECTOR, 'time[datetime="2023-09-15T00:00:00.000"]')
    offers_arrivals_from_date.click()
    offers_arrivals_to_date = driver.find_element(By.CSS_SELECTOR, 'time[datetime="2023-09-23T00:00:00.000"]')
    offers_arrivals_to_date.click()
    dropdown_date_period_arrivals_submit = driver.find_element(By.CSS_SELECTOR,
                                                                'button[data-testid="dropdown-window-button-submit"]')
    dropdown_date_period_arrivals_submit.click()

    time.sleep(2)

    global_search_button_submit = driver.find_element(By.CSS_SELECTOR,
                                                               'button[data-testid="global-search-button-submit"]')
    global_search_button_submit.click()
    time.sleep(15)
    offer = driver.find_element(By.CSS_SELECTOR,'div[data-testid="offer-tile"]').text
    hotel = driver.find_element(By.CLASS_NAME, 'offer-tile-body__header').text
    country = driver.find_element(By.CSS_SELECTOR, 'nav[data-testid="offer-tile-breadcrumbs"]').text
    trip_advisor_opinion = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tripadvisor-opinions-badge"]').text
    price = driver.find_element(By.CSS_SELECTOR, 'span[data-testid="price-amount"]').text.replace(" ", "")
    board_type = driver.find_element(By.CSS_SELECTOR, 'span[data-testid="offer-tile-boardType"]').text
    offer_dates = driver.find_element(By.CSS_SELECTOR, 'span[data-testid="offer-tile-departure-date"]').text

    print(offer)

    time.sleep(300)
    driver.quit()


init_driver("https://www.tui.pl/")

