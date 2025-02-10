import fpabart as bart
import modules.appium_driver.appium_driver_helper as appium_driver_helper
from time import sleep
import random

@bart.scenario("Alert appears when Dry Cycle complete")
def test_end_alert(appium_driver):
 
    # Verify that I am on the running cycle page
    bart.step("Check I am on the running cycle page")
    appium_driver_helper.get_element(appium_driver, "cycle-time-remaining")
    appium_driver_helper.get_element(appium_driver, "button-cancel")
    appium_driver_helper.get_element(appium_driver, "button-options")
    sleep(3)

    # Check that end of cycle menu popup
    bart.step("Check end cycle menu pops up")
    appium_driver_helper.get_element(appium_driver, "Add more item")
    appium_driver_helper.get_element(appium_driver, "Cancel")


@bart.scenario("Close complete with X button")
def test_end_XBtn(appium_driver):

@bart.scenario("Close complete with Done button")
def test_end_Done(appium_driver):

@bart.scenario("Close complete and add more time")
def test_end_addTime(appium_driver):

@bart.scenario("Complete alert popsup after add more time completed")
def test_end_alertComplete(appium_driver):