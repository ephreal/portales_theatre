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
    driver.get("https://theatre.needs.management/login/")

#################################
# GIVEN user info page
# WHEN user click on Admin API test page
# THEN check that user goes to http://localhost:5001/api/admin/test/
#################################

#################################
# GIVEN login page
# WHEN login in
# THEN goes to index page
#################################


def test_valid_valid(test_setup):
    driver.find_element(
            by=By.XPATH,
            value="//input[@id='email']").send_keys("Client@fakemail.com")
    driver.find_element(
            by=By.XPATH,
            value="//input[@id='password']").send_keys("12345678")
    driver.find_element(
            by=By.XPATH,
            value="//input[@class='wtsubmit']").send_keys(Keys.RETURN)


def test_user():
    driver.find_element(
            by=By.XPATH,
            value="//ul/li[4]").click()


def test_first_name():
    driver.find_element(
            by=By.XPATH,
            value="// form/div[1]/input").send_keys("TestFirstName")


def test_last_name():
    driver.find_element(
            by=By.XPATH,
            value="// form/div[2]/input").send_keys("TestLastName")


def test_address_name():
    driver.find_element(
            by=By.XPATH,
            value="// form/div[3]/input").send_keys("TestAddress")


def test_apartment_name():
    driver.find_element(
            by=By.XPATH,
            value="// form/div[4]/input").send_keys("TestApartment")


def test_state():
    driver.find_element(
            by=By.XPATH,
            value="// form/div[5]/input").send_keys("TestST")


def test_city():
    driver.find_element(
            by=By.XPATH,
            value="// form/div[6]/input").send_keys("TestCity")


def test_zip_code():
    driver.find_element(
            by=By.XPATH,
            value="// form/div[7]/input").send_keys("88001")


def test_submit():
    driver.find_element(
            by=By.XPATH,
            value="// form/div[8]/input").click()


def test_edit_word():
    driver.find_element(
            by=By.PARTIAL_LINK_TEXT,
            value="Edit Password").click()
    driver.quit()
