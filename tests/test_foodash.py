import pytest
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://52.64.176.76"

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

def test_01_homepage_loads():
    driver = get_driver()
    driver.get(BASE_URL)
    assert driver.find_element(By.TAG_NAME, "body")
    driver.quit()

def test_02_page_has_title():
    driver = get_driver()
    driver.get(BASE_URL)
    assert driver.title is not None
    driver.quit()

def test_03_root_div_exists():
    driver = get_driver()
    driver.get(BASE_URL)
    assert driver.find_element(By.ID, "root")
    driver.quit()

def test_04_login_page_loads():
    driver = get_driver()
    driver.get(BASE_URL + "/login")
    time.sleep(2)
    assert driver.find_element(By.TAG_NAME, "body")
    driver.quit()

def test_05_login_has_email_field():
    driver = get_driver()
    driver.get(BASE_URL + "/login")
    time.sleep(2)
    field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
    assert field.is_displayed()
    driver.quit()

def test_06_login_has_password_field():
    driver = get_driver()
    driver.get(BASE_URL + "/login")
    time.sleep(2)
    field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    assert field.is_displayed()
    driver.quit()

def test_07_login_has_submit_button():
    driver = get_driver()
    driver.get(BASE_URL + "/login")
    time.sleep(2)
    btn = driver.find_element(By.CSS_SELECTOR, "button")
    assert btn.is_enabled()
    driver.quit()

def test_08_login_invalid_credentials():
    driver = get_driver()
    driver.get(BASE_URL + "/login")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys("invalid@test.com")
    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("wrongpass123")
    buttons = driver.find_elements(By.CSS_SELECTOR, "button")
     for btn in buttons:
      if btn.is_displayed() and btn.is_enabled():
         btn.click()
         break
    time.sleep(3)
    body = driver.find_element(By.TAG_NAME, "body").text.lower()
    assert any(w in body for w in ["invalid", "error", "incorrect", "wrong", "failed", "login"])
    driver.quit()

def test_09_register_page_loads():
    driver = get_driver()
    driver.get(BASE_URL + "/register")
    time.sleep(2)
    assert driver.find_element(By.TAG_NAME, "body")
    driver.quit()

def test_10_register_has_text_field():
    driver = get_driver()
    driver.get(BASE_URL + "/register")
    time.sleep(2)
    field = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
    assert field.is_displayed()
    driver.quit()

def test_11_register_has_email_field():
    driver = get_driver()
    driver.get(BASE_URL + "/register")
    time.sleep(2)
    field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
    assert field.is_displayed()
    driver.quit()

def test_12_register_has_password_field():
    driver = get_driver()
    driver.get(BASE_URL + "/register")
    time.sleep(2)
    field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    assert field.is_displayed()
    driver.quit()

def test_13_homepage_has_heading():
    driver = get_driver()
    driver.get(BASE_URL)
    time.sleep(2)
    headings = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3")
    assert len(headings) > 0
    driver.quit()

def test_14_page_has_navigation():
    driver = get_driver()
    driver.get(BASE_URL)
    time.sleep(2)
    nav = driver.find_element(By.CSS_SELECTOR, "nav, header")
    assert nav.is_displayed()
    driver.quit()

def test_15_api_responds():
    try:
        req = urllib.request.urlopen("http://52.64.176.76/api/restaurants", timeout=5)
        assert req.status == 200
    except urllib.error.HTTPError as e:
        assert e.code in [401, 403]
