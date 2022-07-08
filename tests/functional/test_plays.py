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
    driver.get("https://theatre.needs.management/plays/")


#################################
# GIVEN info
# WHEN user click on currently available plays
# THEN check that user goes to http://localhost:5001/play/1
#################################


def test_available_plays(test_setup):
    driver.find_element(
            by=By.XPATH,
            value="// p[@class='play_display-link']").click()
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
