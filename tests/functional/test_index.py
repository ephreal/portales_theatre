###############################
# Imports
###############################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pytest


@pytest.fixture
def test_setup():
    global driver
    s = Service('/Users/chromedriver')
    driver = webdriver.Chrome(service=s)
    driver.get("https://theatre.needs.management")

#################################
# GIVEN index page
# WHEN user click on Admin API test page
# THEN check that user goes to http://localhost:5001/api/admin/test/
#################################


def test_admin_link(test_setup):
    driver.find_element(
            by=By.LINK_TEXT,
            value="Admin API test page").click()
    driver.quit()

#################################
# GIVEN given index page
# WHEN user click on Client API test page
# THEN check that user goes to http://localhost:5001/api/client/test
#################################


def test_client_link(test_setup):
    driver.find_element(
            by=By.LINK_TEXT,
            value="Client API test page").click()
    driver.quit()

#################################
# GIVEN given index page
# WHEN user click on The place holder link
# THEN check that user goes to http://localhost:5001/awETR3w4wtegZW#56ews
#################################


def test_place_holder(test_setup):
    driver.find_element(
            by=By.PARTIAL_LINK_TEXT,
            value="This link").click()
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
