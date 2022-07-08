###############################
# Issue with unselecting seats. The first 48 will unselect, but the last 48
# will not.
###############################

# Still need to test function of shop cart

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


###############################
# GIVEN seats
# WHEN user selects a seat
# THEN seats will be orange and selected
###############################

def test_click_seat():
    driver.get("https://theatre.needs.management/play/1")
    count = 1
    while count < 97:
        element = f"// section/div[@seat={count}]"
        driver.find_element(
                by=By.XPATH,
                value=(element)).click()
        count += 1

# This test is dependent of the first one

###############################
# GIVEN seats
# WHEN user unselects a seat
# THEN seats will be blue and unselected
###############################

# seats will not unclick and stay orange


def test_unclick_seat():
    count = 1
    while count < 97:
        element = f"// section/div[@seat={count}]"
        driver.find_element(
                by=By.XPATH,
                value=(element)).click()
        count += 1
