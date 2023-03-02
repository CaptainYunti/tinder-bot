from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
import time
import os

# EMAIL = os.environ.get("EMAIL")
# PASSWORD = os.environ.get("PASSWORD")
WINDOWS_USER = "panie"


options = Options()
options.add_experimental_option("detach", True)
options.add_argument(f"--user-data-dir=C:/Users/{WINDOWS_USER}/AppData/Local/Google/Chrome/User Data/")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

wait = WebDriverWait(driver, 10)
short_wait = WebDriverWait(driver, 4)

driver.maximize_window()

driver.get("https://tinder.com")

# Logowanie


def change_window():
    for window in driver.window_handles:
        if window != original_window:
            driver.switch_to.window(window)
            break


try:
    short_wait.until(EC.url_contains("app"))
except selenium.common.exceptions.TimeoutException:

    original_window = driver.current_window_handle

    # wait.until_not(EC.NoSuchElementException)
    driver.implicitly_wait(4)
    driver.find_element(By.CSS_SELECTOR, " a.c1p6lbu0").click()

    try:
        driver.find_element(By.CSS_SELECTOR, "iframe").click()
    except selenium.common.exceptions.ElementNotInteractableException:
        iframe = driver.find_element(By.CSS_SELECTOR, "#credential_picker_container iframe")
        driver.switch_to.frame(iframe)
        driver.find_element(By.ID, "close").click()
        driver.switch_to.parent_frame()
        driver.implicitly_wait(4)
        driver.find_element(By.CSS_SELECTOR, "iframe").click()

    change_window()

    driver.find_element(By.CLASS_NAME, "fFW7wc-ibnC6b-sM5MNb").click()

    driver.switch_to.window(original_window)

# Likowanie

want_more = True
strange_number = 3
error_number = 0
max_error_number = 10

time.sleep(6)

while want_more:
    try:
        driver.find_element(
            By.XPATH,
            f'//div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[{strange_number}]/div/div[4]/button'

        ).click()
        error_number = 0
        time.sleep(1)
    except selenium.common.exceptions.NoSuchElementException:
        error_number += 1
        print(error_number)
        strange_number = 4 if strange_number == 3 else 3
    except selenium.common.exceptions.ElementClickInterceptedException:
        driver.implicitly_wait(2)
        try:
            driver.find_element(By.XPATH, '//main/div/div[3]/button[2]').click()
            want_more = False
        except selenium.common.exceptions.NoSuchElementException:
            try:
                driver.find_element(By.XPATH, '//main/div/div/div[3]/button[2]').click()
            except selenium.common.exceptions.NoSuchElementException:
                driver.refresh()

    if error_number >= max_error_number:
        want_more = False

# Wylogowywanie

driver.implicitly_wait(10)
driver.find_element(By.CSS_SELECTOR, 'a[href="/app/profile"]').click()
driver.implicitly_wait(10)
driver.find_elements(By.CSS_SELECTOR, 'aside div[role="button"]')[-2].click()
driver.implicitly_wait(10)
driver.find_element(By.CSS_SELECTOR, "button.c1p6lbu0").click()

time.sleep(2)
driver.quit()
