###############################
# Imports
###############################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import pytest


@pytest.fixture
def test_setup():
    global driver
    s = Service('/Users/chromedriver')
    driver = webdriver.Chrome(service=s)
    driver.get("https://theatre.needs.management/signup/")

#################################
# GIVEN info
# WHEN user registers for account
# THEN check that user can register
#################################


def test_valid(test_setup):
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='first_name']").send_keys("first")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='last_name']").send_keys("last")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='email']").send_keys("email")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='address']").send_keys("address")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='apartment']").send_keys("apartment")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='city']").send_keys("city")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='state']").send_keys("state")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='zip_code']").send_keys("88001")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='password']").send_keys("password")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='confirmation']").send_keys("password")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='submit']").send_keys(Keys.RETURN)
    driver.quit()


#################################
# GIVEN info
# WHEN user registers for account
# THEN check that user cannot register since user exist
#################################

def test_user_exist(test_setup):
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='first_name']").send_keys("first")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='last_name']").send_keys("last")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='email']").send_keys("email")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='address']").send_keys("address")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='apartment']").send_keys("apartment")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='city']").send_keys("city")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='state']").send_keys("state")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='zip_code']").send_keys("88001")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='password']").send_keys("password")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='confirmation']").send_keys("password")
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='submit']").send_keys(Keys.RETURN)
    driver.quit()

#################################
# GIVEN info
# WHEN user leaves textbox blank
# THEN check that an error is given
#################################


def test_empty_fields(test_setup):
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='submit']").send_keys(Keys.RETURN)
    driver.quit()

#################################
# GIVEN info
# WHEN user enter integers in zip code
# THEN check that an error is given
#################################


def test_invalidInt(test_setup):
    driver.find_element(
            by=By.XPATH,
            value="//input[@name='zip_code']").send_keys(88001)
    driver.quit()

#################################
# GIVEN info
# WHEN user click on home
# THEN check that user goes to http://localhost:5001
#################################


def test_home(test_setup):
    driver.find_element(
            by=By.LINK_TEXT,
            value="Home").click()
    driver.quit()

#################################
# GIVEN info
# WHEN user click on plays
# THEN check that user goes to http://localhost:5001/plays/
#################################


def test_plays(test_setup):
    driver.find_element(
            by=By.LINK_TEXT,
            value="Plays").click()
    driver.quit()

#################################
# GIVEN info
# WHEN user click on about
# THEN check that user goes to http://localhost:5001/about/
#################################


def test_about(test_setup):
    driver.find_element(
            by=By.LINK_TEXT,
            value="About").click()
    driver.quit()

#################################
# GIVEN info
# WHEN user click on login
# THEN check that user goes to http://localhost:5001/login/
#################################


def test_login(test_setup):
    driver.find_element(
            by=By.LINK_TEXT,
            value="Login").click()
    driver.quit()
