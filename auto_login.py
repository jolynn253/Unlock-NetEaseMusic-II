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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DB4CAAC3C0AFA52B187D763E12B473B87EEE42EC642C17A627C5369B35FDD132339576858A485B5FCBC89C454672C1C0063905B28F998ED5EB4C916D9253C875A2DC4BC4CF52392CBB0DEF2FD905FFA586F949C9599FD5AE5FF35B39B415B9AD23E74A54629EEE8FF7394E348ED0B858A3DFDDF3146E178DC48E30CA15B49C60C2F5C4BDE29E4E99B8EB21B88FC30B7755395E833E111737DAD4E233B0E97740B22E7B6B6D8BC06033EC20AF9985E9962BFECC6D725991FCA332342BC625D84FE31A2A5285D251FD56F647D65C854A735A6F31F206485BC205B828680DC47A2DE10A6F4BA4B6B7B57B665D0C80EAEA491FFCA377F8DB4008A982396ABBA6A7CAE50F9DFC09A50F77CBB6FE1F06F443F6DACDDEDDCEFB503055CDF5EE6ED1394120F1DB781E202AF4A5F020C2D63A4A91FBF31F8F393D9029EE8FE7431D1C0B9F46491F4E77DE70993A4661BF9EB7783AFD5DEADF447E61A0082D440A0CEAE0C1C176A1CD15A9941D1184E889CCEF347399F67439E719E3D10048F00B432C91B87A4F05636E7343B05959723A8E20E2D7
"})
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
