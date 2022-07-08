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
# GIVEN an email and password box
# WHEN a user logs in
# THEN check that user can log in
#################################


def test_signin(test_setup):
    driver.find_element(
            by=By.XPATH,
            value="//input[@id='email']").send_keys("client@fakemail.com")
    driver.find_element(
            by=By.XPATH,
            value="//input[@id='password']").send_keys("12345678")
    driver.find_element(
            by=By.XPATH,
            value="//input[@class='wtsubmit']").send_keys(Keys.RETURN)

#################################
# GIVEN an index page
# WHEN a user clicked on shopping cart
# THEN user will go selected seats
#################################


def test_shopping_cart():
    driver.find_element(
            by=By.XPATH,
            value='// aside/a').click()


#################################
# GIVEN selected seats in shopping cart
# WHEN clicks purchased seats
# THEN seats will be purchased
#################################
def test_purchase_seat():
    driver.find_element(
            by=By.XPATH,
            value='// section/button').click()
