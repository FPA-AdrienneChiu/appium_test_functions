import fpabart as bart
import modules.appium_driver.appium_driver_helper as appium_driver_helper
from appium.webdriver import Remote

from time import sleep



@bart.scenario("Running Auto")
def test_running_auto(appium_driver: Remote):
    """Test dryers run cycle and verify UI elements"""

    #Verify I am on Home Screen 
    appium_driver_helper.verify_text(appium_driver, "DRYER", "DRYER")

    # Navigate from the Home Screen to the Material Settings Screen
    material_panel_id = "Mixed"
    appium_driver_helper.get_element(appium_driver, material_panel_id).click()

    # Press button selecting Mixed
    mixed = appium_driver_helper.get_element(appium_driver, "Mixed", "Mixed") #chnage element  
    mixed.click()

    # Verify that the time is set to "AUTO"
    appium_driver_helper.verify_text(appium_driver, "time", "time")
    appium_driver_helper.verify_text(appium_driver, "Auto", "Auto" )

    # Click on Start button
    start = appium_driver_helper.get_element(appium_driver, "Start")
    start.click()

    # Verify I am on Running Cycle Screen
    appium_driver_helper.verify_text(appium_driver, "Cancel", "Cancel")
    appium_driver_helper.verify_text(appium_driver, "Options", "Options")
    appium_driver_helper.verify_text(appium_driver, "Add item", "Add item")

    #  Wait for 30 seconds of no interaction
    sleep(30)

    # Check footer and hamburger menu dissapears

   