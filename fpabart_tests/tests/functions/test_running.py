import fpabart as bart
import modules.appium_driver.appium_driver_helper as appium_driver_helper
from appium.webdriver import Remote
from time import sleep



@bart.scenario("Running Auto")
def test_running_auto(appium_driver: Remote):
    """Test dryers run cycle and verify UI elements"""

    #Verify I am on Home Screen 
    bart.step("Check if on Home Screen")
    appium_driver_helper.verify_text(appium_driver, "DRYER", "DRYER")

    # Navigate from the Home Screen to the Material Settings Screen
    bart.step("Check for mixed material")
    material_panel_id = "Mixed"
    appium_driver_helper.get_element(appium_driver, material_panel_id).click()

    # Press button selecting Mixed
    bart.step("Click on mixed material")
    mixed = appium_driver_helper.get_element(appium_driver, "Mixed", "Mixed") #chnage element  
    mixed.click()

    # Verify that the time is set to "AUTO"
    bart.step("Check if time is set to Auto")
    appium_driver_helper.verify_text(appium_driver, "time", "time")
    appium_driver_helper.verify_text(appium_driver, "Auto", "Auto" ) #first Auto should be time id first

    # Click on Start button
    bart.step("Click start")
    start = appium_driver_helper.get_element(appium_driver, "Start")
    start.click()

    # Verify I am on Running Cycle Screen
    bart.step("Check for running cycle menu text")
    appium_driver_helper.verify_text(appium_driver, "Cancel", "Cancel")
    appium_driver_helper.verify_text(appium_driver, "Options", "Options")
    appium_driver_helper.verify_text(appium_driver, "Add item", "Add item")

    #  Wait for 30 seconds of no interaction
    bart.step("Wait 30 secs to sleep")
    sleep(30)

    # Check footer and hamburger menu dissapears
    bart.step("footer and hamburger menu dissapears")


   # change to resource_id, so far test has failed