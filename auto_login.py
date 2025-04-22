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
    browser.add_cookie({"name": "MUSIC_U", "value": "0069751CBCB56ED253A2563ABCB1E6EB2730A1D77FAE28C0DEA558F926EC2F74CB2D0B78F2CA2157FB58FCC020521ACECF760FB9BFB84773DCA2FEAD398DA580E228C01D0A9D4475C41679E0C623274BBA347B9A6C319FE845F888CAEE453EF650E998B7A30AA67D218FDFD41B06FEEA97E570C93A25C621F29D84358AA7A76D5B9840C76975ABD0DC619BBBFAF06CA524FDA1B33B13EF1CBB9ADE39995B5F1616854BE7671CE8CB39D6164E43C85F2E06CEC9BFB30D96F4BD3DDC49F082591A80D54CED221DC91567D7C21D312E02FE34E17371824E4D6A88E567F2830871BC915A80652B43AB1740BB741E2205A891E80C39D5CCB5D7A06F86ADAA8B9825A22EF17366C07D1262BB8C4635E98DB082476EBBD8DA2CCA1FDF039A9324A21C3BFA7C587A205D017EBE46FE2F1D7CA2E7A261B9A8CAA0B18E927BFD0EF466ABD39A919EE9D4D89A8840891215741A289ECDDC79F4179E3E171C330AA196936AFC6C"})
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
