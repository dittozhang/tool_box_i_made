import time
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait_a_sec = 0.5
driver.get("https://web.telegram.org/k/")
# login info
country = "Taiwan"
phone_number = "+886 983 003 752"


def found_element(by_what: object, element_name: str):
    while True:
        try:
            element = driver.find_element(by_what, element_name)
            return element
        except NoSuchElementException:
            time.sleep(wait_a_sec)
            continue
        except Exception as e:
            print(f"[Error] {e}")
            exit(1)
        else:
            print(f"[+]Found {element_name}")


# telegram login page
try:
    login_by_phonenum_btn = found_element(By.CLASS_NAME, "btn-secondary")
    login_by_phonenum_btn.click()
    select_country_text = found_element(By.CLASS_NAME, "input-field-input")
    select_country_text.send_keys(country)
    phone_number_text = found_element(By.XPATH,
                                      '//*[@id="auth-pages"]/div/div[2]/'
                                      + 'div[2]/div/div[3]/div[2]/div[1]')
    phone_number_text.clear()
    phone_number_text.send_keys(phone_number)
    next_btn = found_element(By.CLASS_NAME, "btn-primary.btn-color-primary.rp")
    next_btn.click()
    code_text = found_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[4]/div/div[3]/div/input')
    code_text.send_keys(input("code: ").strip())
    password_text = found_element(By.NAME, "notsearch_password")
    password_text.send_keys(getpass("password: ").strip())
    next_btn = found_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[5]/div/div[2]/button')
    next_btn.click()
except KeyError:
    pass
    # print(f"[ERROR] {e}")

input("Login first...")
# telegram user page
try:
    tg_setting_btn = found_element(By.CLASS_NAME, "c-ripple")
    tg_setting_btn.click()
    driver.find_element(By.CLASS_NAME, "tgico-settings").click()
    time.sleep(wait_a_sec)
    driver.find_element(By.CLASS_NAME, "tgico-activesessions").click()
    time.sleep(wait_a_sec)
    driver.find_element(By.CLASS_NAME, "tgico-stop").click()
    time.sleep(wait_a_sec)
    driver.find_element(By.CLASS_NAME, "btn.danger.rp").click()
    time.sleep(wait_a_sec)
except Exception as e:
    print(f"[ERROR] {e}")

try:
    alert = "For security reasons, you can't terminate older sessions \
from a device that you've just connected. Please use an earlier \
connection or wait for a few hours."
    popup_msg = driver.find_element(By.CLASS_NAME, "popup-description").text
    if popup_msg == alert:
        print("Terminate All Other Sessions Failure.")
    else:
        print("Terminate All Other Sessions Success.")
except:
    print("Terminate All Other Sessions Success.")

input("pause")
