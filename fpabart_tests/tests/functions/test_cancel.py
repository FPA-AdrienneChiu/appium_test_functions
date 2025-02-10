import fpabart as bart
import modules.appium_driver.appium_driver_helper as appium_driver_helper
from time import sleep
import random

@bart.scenario("Cancel during active cycle")
def test_cancel_active(appium_driver):

    #Check that I am on Home Screen
    bart.step("Check for screen title")
    dyer_title = appium_driver_helper.get_element(appium_driver, "title")

    dyer_title_text = appium_driver_helper.get_text(appium_driver, dyer_title)
    if dyer_title_text == "DRYER":
        print("Home screen title verification passed.")
    else:
        print("Home screen title verification failed.")

    # Check for material options and click one
    bart.step("Check that all materials are present")
    material_options =  ["Mixed", "Cotton", "Polyester", "Elastane", "Silk", "Acrylic", "Viscose"] #wool and cashmere do not have auto
    sleep(1)
    appium_driver_helper.swipe(appium_driver, "Acrylic", "Mixed", 3)
    material_options = ["Linen", "Lyocell", "Down", "Hemp", "Ramie", "Nylon"]
    chosen_material = random.choice(material_options)

    bart.step(f"Selecting random material: {chosen_material}")
    material_element = appium_driver_helper.get_element(appium_driver, chosen_material)
    material_element.click()
    sleep(3)

    # Verify that the time is set to "AUTO"
    bart.step("Check if time is set to Auto")
    Auto = appium_driver_helper.get_element(appium_driver, "Auto")
    appium_driver_helper.get_text(appium_driver, Auto)

    time_selection = appium_driver_helper.get_element(appium_driver, "time")
    appium_driver_helper.get_text(appium_driver, time_selection)

    #Click on Start button
    bart.step("Click start")
    start_btn = appium_driver_helper.get_element(appium_driver, "Start") 
    start_btn.click()
    
    # Verify I am on Running Cycle Screen
    bart.step("Check that I am on running cycle menu")
    appium_driver_helper.get_element(appium_driver, "Auto") # change to time remain
    appium_driver_helper.get_element(appium_driver, "Cancel")
    appium_driver_helper.get_element(appium_driver, "Options")
    appium_driver_helper.get_element(appium_driver, "Add item")

    # Verfify Captouch [NEED TO DO]

    # Click on the cancel button
    bart.step("Click cancel button on active screen")
    cancel_btn = appium_driver_helper.get_element(appium_driver, "Cancel")
    cancel_btn.click()

    # Check for cancel popup 
    bart.step("Check I am on cancel menu")
    appium_driver_helper.get_element(appium_driver, "Cancel the cycle?")
    appium_driver_helper.get_element(appium_driver, "Back")
    appium_driver_helper.get_element(appium_driver, "Cancel cycle")

    # Click on the cancel cycle button
    bart.step("Click cancel button on cancel menu")
    cancel_cycle_btn = appium_driver_helper.get_element(appium_driver, "Cancel cycle")
    cancel_cycle_btn.click()

    # Cycle cancelled screen popups
    bart.step("Check for cancel confirmation popup")
    appium_driver_helper.get_element(appium_driver, "Cycle cancelled")

    # Wait for a few seconds
    bart.step("Wait for machine to process")
    sleep(3)

    # Check I am back on the material selection screen
    bart.step("Check for screen title")
    dyer_title = appium_driver_helper.get_element(appium_driver, "title")

    dyer_title_text = appium_driver_helper.get_text(appium_driver, dyer_title)
    if dyer_title_text == "DRYER":
        print("Home screen title verification passed.")
    else:
        print("Home screen title verification failed.")


# @bart.sceanario("Cancel after Wake Up")
# def test_cancel_wake(appium_driver):
#     # Prior leading steps to be written

#     # Wait for screen to go to sleep
#     bart.step("Wait for screen to go to sleep")
#     sleep(1000)

#     # Wake up screen
#     # captouch step

#     # Verify I am on Running Cycle Screen
#     bart.step("Check that I am on running cycle menu")
#     appium_driver_helper.get_element(appium_driver, "Auto") # change to time remain
#     appium_driver_helper.get_element(appium_driver, "Cancel")
#     appium_driver_helper.get_element(appium_driver, "Options")
#     appium_driver_helper.get_element(appium_driver, "Add item")

#     # Click on the cancel button
#     bart.step("Click cancel button on active screen")
#     cancel_btn = appium_driver_helper.get_element(appium_driver, "Cancel")
#     cancel_btn.click()
    
#     # Click on the cancel cycle button
#     bart.step("Click cancel button on cancel menu")
#     cancel_cycle_btn = appium_driver_helper.get_element(appium_driver, "Cancel cycle")
#     cancel_cycle_btn.click()

#     # Cycle cancelled screen popups
#     bart.step("Check for cancel confirmation popup")
#     appium_driver_helper.get_element(appium_driver, "Cycle cancelled")

#     # Wait for a few seconds
#     bart.step("Wait for machine to process")
#     sleep(3)

#     # Check I am back on the material selection screen
#     bart.step("Check for screen title")
#     dyer_title = appium_driver_helper.get_element(appium_driver, "title")

#     dyer_title_text = appium_driver_helper.get_text(appium_driver, dyer_title)
#     if dyer_title_text == "DRYER":
#         print("Home screen title verification passed.")
#     else:
#         print("Home screen title verification failed.")



# @bart.scenario("Click back and get cancle cycle alert")
# def test_cancel_alert(appium_driver):
# # put in full process later

#     # Verify I am on Running Cycle Screen
#     bart.step("Check that I am on running cycle menu")
#     appium_driver_helper.get_element(appium_driver, "Auto") # change to time remain
#     appium_driver_helper.get_element(appium_driver, "Cancel")
#     appium_driver_helper.get_element(appium_driver, "Options")
#     appium_driver_helper.get_element(appium_driver, "Add item")

#     # Verfify Captouch [NEED TO DO]

#     # Click on the cancel button
#     bart.step("Click back button on active screen")
#     cancel_btn = appium_driver_helper.get_element(appium_driver, "Cancel")
#     cancel_btn.click()

#     # Check for cancel popup 
#     bart.step("Check I am on cancel menu")
#     appium_driver_helper.get_element(appium_driver, "Cancel the cycle?")
#     appium_driver_helper.get_element(appium_driver, "Back")
#     appium_driver_helper.get_element(appium_driver, "Cancel cycle")

#     # Click on the cancel cycle button
#     bart.step("Click cancel button on cancel menu")
#     back_btn = appium_driver_helper.get_element(appium_driver, "Back")
#     back_btn.click()

#     # Verify I am on back on Running Cycle Screen
#     bart.step("Check that I am back on running cycle screen")
#     appium_driver_helper.get_element(appium_driver, "Cancel")
#     appium_driver_helper.get_element(appium_driver, "Options")
#     appium_driver_helper.get_element(appium_driver, "Add item")