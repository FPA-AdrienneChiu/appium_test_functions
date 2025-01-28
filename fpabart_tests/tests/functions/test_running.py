import fpabart as bart
import modules.appium_driver.appium_driver_helper as appium_driver_helper
from time import sleep



@bart.scenario("Running Auto")
def test_running_auto(appium_driver):
    """Test dryers auto run cycle and verify UI elements"""

    #Check I am on Home Screen 
    bart.step("Check if on Home Screen")
    appium_driver_helper.verify_text(appium_driver, "button-menu-title-1", "COTTON") # for DRYER



    # # Navigate from the Home Screen to the Material Settings Screen
    # bart.step("Check for materials")
    # materials = {
    # "option-card-fibre-mixed": "Mixed",
    # "option-card-fibre-cotton": "Cotton",
    # "option-card-fibre-Polyester": "Polyester",
    # "option-card-fibre-Silk": "Silk",
    # "option-card-fibre-Wool": "Wool",
    # "option-card-fibre-Acrylic": "Acrylic",
    # "option-card-fibre-Viscose": "Viscose",
    # "option-card-fibre-Linen": "Linen",
    # "option-card-fibre-Lyocell": "Lyocell",
    # "option-card-fibre-Down": "Down",
    # "option-card-fibre-Hemp": "Hemp",
    # "option-card-fibre-Cashmere": "Cashmere",
    # "option-card-fibre-Nylon": "Nylon",
    # "option-card-fibre-Ramie": "Ramie"
    #}
    # appium_driver_helper.get_element(appium_driver, materials).click()


    # Verify that the time is set to "AUTO"
    # bart.step("Check if time is set to Auto")
    # appium_driver_helper.verify_text(appium_driver, "option-card-time", "time")
    # appium_driver_helper.verify_text(appium_driver, "time", "Auto" ) 

    # Click on Start button
    # bart.step("Click start")
    # start = appium_driver_helper.get_element(appium_driver, "Start") #no resource id
    # start.click()

    # Verify I am on Running Cycle Screen
    # bart.step("Check for running cycle menu text")
    # appium_driver_helper.verify_text(appium_driver, "cycle-time-remaining", "Auto")
    # appium_driver_helper.verify_text(appium_driver, "Cancel", "Cancel") # no resource id
    # appium_driver_helper.verify_text(appium_driver, "Options", "Options") # no resource id
    # appium_driver_helper.verify_text(appium_driver, "Add item", "Add item")# no resource id

    # Wait for 30 seconds of no interaction
    # bart.step("Wait 30 secs to sleep")
    # sleep(30)

    # Check footer and hamburger menu dissapears
    # bart.step("footer and hamburger menu dissapears")
