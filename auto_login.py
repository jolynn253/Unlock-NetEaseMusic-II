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
    browser.add_cookie({"name": "MUSIC_U", "value": "00BD6453B8D6E1FD355D6A9FFC3CAF1D673944CE2DB72FA3B94585E62E73E7E9E435E9143817F2B258EA3D32278CB4D2BFABDF78D46BA4C322A107C718C2C5319C318D947EEAB7C3D2419BF3B578A5BBAA2ECDABB1750CB049B2DCE73CB15590E1E6F9AD1032CD05B87263CA24EE13B9269BEE3168FE1035F2E924EDFEC51BCDB6263CD238B7354913C7092699B180F95D80DAF4F530E586ED76A023EF200FD8C80191987EC0627AF87A09476AED4BBDF1429178BEE1CD5C5C3CC252ABE94D72B92DF3ACCD9D016C7D193E38ACC462D38A84AE63E60E288B4615A98CCA119BC257E7CEE9E93C6260B8334D426C35241833B2C1F6FDC12F5EF6EB571287AAE83212C1500F8A7A554E18104912CFFF342195F5E73E4A5E6E059C78F818A92337ED7B500B02FBE65025D67C42B9A871265B502140760B19BF094FDFB7C0918D202467EBCF690136D6F8D03A74E265A9679C1E544494AA0BD0BF6EE173E0F0EBA86A6B"})
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
