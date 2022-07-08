###############################
# Imports
###############################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.firefox.service import Service
import pytest


# This path is personal, When running use the path to where you saved
# chromedriver
# Mightysteve Path: /Users/chromedriver

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


def test_valid_valid(test_setup):
    driver.find_element(
            by=By.XPATH,
            value="//input[@id='email']").send_keys("asdf@example.com")
    driver.find_element(
            by=By.XPATH,
            value="//input[@id='password']").send_keys("12345678")
    driver.find_element(
            by=By.XPATH,
            value="//input[@class='wtsubmit']").send_keys(Keys.RETURN)
    driver.quit()

#################################
# GIVEN an email and password box
# WHEN a user logs in
# THEN check that user cannot log in with invalid password and gives 'incorrect
# password'
#################################


def test_valid_invalid(test_setup):
    driver.find_element(
            by=By.XPATH,
            value="//input[@id='email']").send_keys("asdf@example.com")
    driver.find_element(
            by=By.XPATH,
            value="//input[@id='password']").send_keys("123456789")
    driver.find_element(
            by=By.XPATH,
            value="//input[@class='wtsubmit']").send_keys(Keys.RETURN)
    driver.quit()

#################################
# GIVEN an email and password box
# WHEN a user logs in
# THEN check that user cannot log in with invalid email and gives 'user does
# not exist'
#################################


def test_invalid_valid(test_setup):
    driver.find_element(
            by=By.XPATH,
            value="//input[@id='email']").send_keys("Notasdf@example.com")
    driver.find_element(
            by=By.XPATH,
            value="//input[@id='password']").send_keys("12345678")
    driver.find_element(
            by=By.XPATH,
            value="//input[@class='wtsubmit']").send_keys(Keys.RETURN)
    driver.quit()

#################################
# GIVEN an email and password box
# WHEN user does not put enouph characters in password box
# THEN check that user cannot log in and express that there is not enough
# characters
#################################


def test_valid_NotEnouphChar(test_setup):
    driver.find_element(
            by=By.XPATH,
            value="//input[@id='email']").send_keys("asdf@example.com")
    driver.find_element(
            by=By.XPATH,
            value="//input[@id='password']").send_keys("123")
    driver.find_element(
            by=By.XPATH,
            value="//input[@class='wtsubmit']").send_keys(Keys.RETURN)
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
