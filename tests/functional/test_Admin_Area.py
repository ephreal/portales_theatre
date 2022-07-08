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
            value="//input[@id='email']").send_keys("asdf@example.com")
    driver.find_element(
            by=By.XPATH,
            value="//input[@id='password']").send_keys("12345678")
    driver.find_element(
            by=By.XPATH,
            value="//input[@class='wtsubmit']").send_keys(Keys.RETURN)


#################################
# GIVEN index page
# WHEN Admin area is clicked
# THEN goes to Admin area/site administration
#################################
def test_admin_area_link():
    driver.find_element(
            by=By.LINK_TEXT,
            value="Admin Area").click()


#################################
# GIVEN Admin area/site administration
# WHEN Users box with picture is clicked
# THEN shows current administrators and users
#################################
def test_Users():
    driver.find_element(
            by=By.XPATH,
            value="//section/section/a[1]").click()

#################################
# GIVEN Administrators and Users
# WHEN Edit User button is clicked
# THEN shows text boxed to change information
#################################


def test_edit_button():
    driver.find_element(
            by=By.XPATH,
            value="// section/section[1]/section[3]/button[1]").click()


#################################
# GIVEN Administrators and Users
# WHEN Edit User button is clicked
# THEN shows text boxed to change information
#################################

# Could add highlighting to edit textboxes

def test_valid():
    driver.find_element(
            by=By.XPATH,
            value="//section/form/div[1]/input[@value]").send_keys(Keys.BACKSPACE * 10 + "asdf")

    driver.find_element(
            by=By.XPATH,
            value="//section/form/div[2]/input[@value]").send_keys(Keys.BACKSPACE * 10 + "Evans")

    driver.find_element(
            by=By.XPATH,
            value="//section/form/div[3]/input[@value]").send_keys(Keys.BACKSPACE * 10 + "Address")

    driver.find_element(
            by=By.XPATH,
            value="//section/form/div[4]/input[@value]").send_keys(Keys.BACKSPACE * 10 + "Apartment")

    driver.find_element(
            by=By.XPATH,
            value="//section/form/div[5]/input[@value]").send_keys(Keys.BACKSPACE * 2 + "NM")

    driver.find_element(
            by=By.XPATH,
            value="//section/form/div[6]/input[@value]").send_keys(Keys.BACKSPACE * 10 + "Las Cruces")

    driver.find_element(
            by=By.XPATH,
            value="//section/form/div[7]/input[@value]").send_keys(Keys.BACKSPACE * 10 + "88888")

    driver.find_element(
            by=By.XPATH,
            value="//section/form/div[8]/input[@value]").click()

    # Getting an error
    driver.find_element(
            by=By.XPATH,
            value="//section/form/p").click()

#################################
# GIVEN Change Password
# WHEN text boxes are edited and button is clicked
# THEN green prompt will show password is update
#################################

    driver.find_element(
            by=By.XPATH,
            value="// section/form/div[1]/input").send_keys("12345678")

    driver.find_element(
            by=By.XPATH,
            value="// section/form/div[2]/input").send_keys("12345678")

    driver.find_element(
            by=By.XPATH,
            value="// section/form/div[3]/input").click()

#################################
# GIVEN Admin area/site administration
# WHEN Back box with picture is clicked
# THEN website goes back to index page
################################


def test_back():
    driver.get("https://theatre.needs.management/admin/")
    driver.find_element(
            by=By.XPATH,
            value='// section/section/a[3]').click()


#################################
# GIVEN Admin area/site administration
# WHEN shedule box with picture is clicked
# THEN clickable plays show
################################


def test_Schedule():
    driver.get("https://theatre.needs.management/admin/")
    driver.find_element(
            by=By.XPATH,
            value='// section/section/a[2]').click()

#################################
# GIVEN Plays
# WHEN play is clicked
# THEN seats and selected seat editor show
################################


def test_plays():
    driver.find_element(
            by=By.XPATH,
            value='// section/section/section[5]/a').click()

#################################
# GIVEN seats and selected seat editor
# WHEN seats are clicked
# THEN seats will turn green and counter for selected will increase by 1
# and total selected price will increse by n pricing
################################


def test_click_seat():
    count = 1
    while count < 97:
        element = f"// section/div[@seat={count}]"
        driver.find_element(
                by=By.XPATH,
                value=(element)).click()
        count += 1

#################################
# GIVEN seats and selected seat editor
# WHEN seats are selected unselect seat
# THEN seats will turn blue and counter for selected will decrease by 1
################################


def test_unclick_seat():
    count = 1
    while count < 97:
        element = f"// section/div[@seat={count}]"
        driver.find_element(
                by=By.XPATH,
                value=(element)).click()
        count += 1


#################################
# GIVEN seats and Selected Seat Editor
# WHEN Selecting a date drop box is clicked
# THEN drop box shows dates
################################


def test_date():
    driver.find_element(
            by=By.XPATH,
            value='// section/aside[1]/section/div/div[1]/select').click()


#################################
# GIVEN seats and Selected Seat Editor
# WHEN Select a time drop box is clicked
# THEN drop box shows times
################################


def test_time():
    driver.find_element(
            by=By.XPATH,
            value='// section/aside[1]/section/div/div[2]/select').click()


#################################
# GIVEN seats and Selected Seat Editor
# WHEN Selecting a pricing text box
# THEN able to input new pricing
################################


def test_Pricing():
    driver.find_element(
            by=By.XPATH,
            value='// section[1]/section/div/input').send_keys("90")


#################################
# GIVEN seats and Selected Seat Editor
# WHEN clicking Update Pricing
# THEN Pricing for seat will update
################################


def test_update_pricing():
    driver.find_element(
            by=By.XPATH,
            value='// section[1]/section/div/input').click()


#################################
# GIVEN seats and Selected Seat Editor
# WHEN clicking Seating
# THEN will bring you to seating page
################################


def test_seating():
    driver.find_element(
            by=By.XPATH,
            value='// aside/ul/li[1]').click()


#################################
# GIVEN seats and Selected Seat Editor
# WHEN clicking Details
# THEN will stay on same page
################################


def test_details():
    driver.find_element(
            by=By.XPATH,
            value='// aside/ul/li[2]').click()


#################################
# GIVEN Modify Play Information
# WHEN Name is modified
# THEN Name will change to new inputed name
################################


def test_mod_name():
    driver.find_element(
            by=By.XPATH,
            value='// form/div/input').send_keys("New Name")


#################################
# GIVEN Modify Play Information
# WHEN Date is modified
# THEN date will change
################################


def test_mod_date():
    driver.find_element(
            by=By.XPATH,
            value='// table/tbody/tr/td/input').click()

#################################
# GIVEN Modify Play Information
# WHEN Add date is clicked
# THEN you will go to seats page
################################


def test_add_date():
    driver.find_element(
            by=By.XPATH,
            value='// div/button').click()

#################################
# GIVEN Modify Play Information
# WHEN time is clicked and input at 1
# THEN the time will change to 1 pm
################################
# When times were changed and internal server error showed

'''
def test_update_times():
    driver.find_element(
            by=By.XPATH,
            value="//div/ul[@id='times']/li/table/tbody/tr/td/input").click()
'''

#################################
# GIVEN Modify Play Information
# WHEN default price ins clicked
# THEN input keys which will change the price
################################

'''
def test_update_default_price():
    driver.find_element(
            by=By.XPATH,
            value="// form/div[4]/input").click().send_keys('90')
'''

#################################
# GIVEN Modify Play Information
# WHEN default price ins clicked
# THEN input keys which will change the price
################################

'''
def test_update_description():
    driver.find_element(
            by=By.XPATH,
            value="// form/div[6]/textarea").click().send_keys('New Description')
'''
#################################
# GIVEN Modify Play Information
# WHEN active? checkbox is clicked when active
# THEN check box will turn white and turn unactive
################################

'''
def test_not_active():
    driver.find_element(
            by=By.XPATH,
            value="// form/div[7]/input").click()

'''
#################################
# GIVEN Modify Play Information
# WHEN active? checkbox is clicked when unactive
# THEN check box will turn green and turn active
################################

'''
def test_active():
    driver.find_element(
            by=By.XPATH,
            value="// form/div[7]/input").click()
'''
#################################
# GIVEN Modify Play Information
# WHEN active? checkbox is clicked when unactive
# THEN check box will turn green and turn active
################################

'''
def test_edit_play():
    driver.find_element(
            by=By.XPATH,
            value="// form/div[8]/input").click()
'''
#################################
# GIVEN Admin area/site administration
# WHEN log out box with picture is clicked
# THEN log out of account
################################


def test_logout():
    driver.get("https://theatre.needs.management/admin/")
    driver.find_element(
            by=By.XPATH,
            value='// section/section/a[4]').click()
