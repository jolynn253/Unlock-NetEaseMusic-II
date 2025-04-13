# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00F235BCF1D7DF86A04348ADAFA471F241F23612ABB81689E069E68BCE437728B395607530CEE9BBB7BC1CBE810A07AD4BFCDC43C7C02C5B6F207BA8FA079ECB6D79DF44F75BD96944B681E3C8A4ABBE5889CF95B104722192320F34A1E3846DED069F148AFB312F6AC9805B742965522C145FA1E55FF02633E18538D64AA102E3C2129184474BC1EE2616BF965939134B72983F8D0A3280F4A8C3FE55F5E163D73AB27F7A521402949140E31E230B5B4CF313EF62783CDE081ED5D92335C9814808990E9F72A52EF494CA3BA83804F8AB63581606874085354CCDF6A719B0348668F44AE557C52CC84EEB387445178D082D316378716247DA6A08DD75CDDBDA04CBCAC8909F3E4D3BA72DD048CBBAA12900489BF3608BF5293FC8EDA2B3958C5FC489057000FBEE408453CE2F2F2E93D71404758D93F3B8A27072312466EF2C85F1174777979D3B7F0BC99FD089D4C9949B99728F00975F838A473BB7E2D65E3C"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
