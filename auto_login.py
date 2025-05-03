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
    browser.add_cookie({"name": "MUSIC_U", "value": "004647C48A07278E339B515A23A95A07DA2CC8C5D9CD6218C5F736E41DD5956F10176D29B45E4470C88CCF20563CC3DF594104245EB16A283F0B6184EB74FF4D7AFE2E8BCFA9D922452021D7F14B2EBCA34FAA2BFF23D3D89FDAFC66CB0296AED3A7ACEAC4DB507F281BC5B23C8D08DCD9510A48F97FB5D5EE142E27915C866814EDEBF9E3FD9552BB70BEB240BB83570FC641911FE2D5F6F14DD81F1FD6AD09EE9689A467EDEB7EFAAB58C87555F38628871EB2C66F93A19ACDC7B71AAB6ED3A8CE2846F78249DAE21090E5611E64A367EEECB9E4EB398E6A7D24B13B286331B1EDEF60B9E2473AE95A564863EDA977EEB53841EDBDAB9AB154109C36085DF7157F8EF223915B14A2FD54DE51DAA8DADA1CB0A86B41E35A7914DDE08A485C5EFEF02CF6F71C0984A4CCD48D3778D3C8320CFEEE3C01F316992D342C878CF35A050FCF46B6DBD5D4D7C9F617E99BA4C1412DA1C3C21FCD877EC46F6038AF57E281"})
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
