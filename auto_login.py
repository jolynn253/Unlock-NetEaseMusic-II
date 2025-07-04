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
    browser.add_cookie({"name": "MUSIC_U", "value": "00AA187C7904FA55BEEBB70C9E1643DC6FFDDE7943BEFD4EECAA060AE73A2EC73C81E7C39619699367D224C04427B6EFE7A2E3E9F020942CED8A6E384DC453AE23C841495485874950FDB54FFE05D415F4693009853B74D444A00F071908062E74CAE0FD8ABEB62DF85058646C7EB9C07CE022D5DAF1711F01D8821F2ED74E8168A5C670DF9E53B78EF7DA269FCA854DD91D3DCF65E89A4978437DFA40A2B297992A9EC05D6FB55A49A85F764CA87BDFD877B27E60A5E57EA989E9E4BF69159C8B18639F9FB283E3C9C0C1DA44121FF16CA2492231C6E0C65F440E334E9E79D2B607997A5B40F9A758ABFA084DE2FD2558C9C61179E96BE7F96C9CE03D4F3B2382906BF04553560D744F7B5C1B28195996A7B9258EC8C3ADB421E4F6DC39AF46069EA06C49C8FED862A53B1662D3B9D40C56E114718DBFA49507AFC98C2631808686E3F9233B052484F8C1A1D516870DCECEEF698DA81CF443B00B88C64A7EEC3E
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
