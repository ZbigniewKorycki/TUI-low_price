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
    chrome_driver_path = "/Users/zbigniewkorycki/Downloads/chromedriver_mac64"
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 3)
    driver.get(link_to_scrape)
    driver.maximize_window()
    time.sleep(300)
    driver.quit()


init_driver("https://www.tui.pl/")
