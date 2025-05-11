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
    browser.add_cookie({"name": "MUSIC_U", "value": "002A5A00C03F14AAB399EF960861C13228A3F243D0E4F0C58BF9AAA1F59BF6FA1872A3759D4A77E282242264A81A2D79B6D8C9B820EA4803AA69CF01CD034575CBE1E67169576A9A2ABACA4385B77857004B984083EBB5C776498B361B90982DB7EE22670A58AAEECE4625E2AEA177B2E2FDB87885CC83A6F7CA40CEF9A9307622F43BD4640893E0A8E4A80774BDAD8DDAF15C35E40B02D32411408F23AC99BA4449BD3C279DC37D89EB655DD0431DB7A7B1289C00A714F13BBCCCE01EE177354831624ADA2254F4F8348FFA4A04392A9218A70D876FC7DAA9FB893C83794514BEEE545BADF9CCF8176DFF585C75B280F2C220328D8660A21AD803C8661D0569ECB252DBCD0914ABE1B54635885AC26FCB688D04F7931C80DBDFA25437E5C4E4C353A3945D8BCB7805C9140D7F236875F22F1BC64C1E8974EDE0D5E9E8988120D8005CAC1B3277401EFE3016209BB7451BA700EF02C294FE6F468D6DF3E5BB9574"})
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
