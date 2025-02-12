import fpabart as bart
import modules.appium_driver.appium_driver_helper as appium_driver_helper
from time import sleep
import random

@bart.scenario("Cancel during active cycle")
def test_cancel_active(appium_driver):
    """Cancel dry cycle when screen is active """

    # Place in logic from running.py
    
    # Click on the cancel button
    bart.step("Click cancel button on active screen")
    cancel_btn = appium_driver_helper.get_element(appium_driver, "Cancel")
    cancel_btn.click()

    # Check for cancel popup 
    bart.step("Check I am on cancel menu")
    appium_driver_helper.get_element(appium_driver, "button-back")
    appium_driver_helper.get_element(appium_driver, "Back")
    appium_driver_helper.get_element(appium_driver, "Confirm")

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



@bart.sceanario("Cancel after Wake Up")
def test_cancel_wake(appium_driver):
    """Cancel Dry cycle after waking up the screen"""
    
    # Place in logic from running.py

    # Wait for screen to go to sleep
    bart.step("Wait for screen to go to sleep")
    sleep(100)

    # Captouch to wake up screen
    # bart.step("Touch screen to wake up")

    # Click on the cancel button
    bart.step("Click cancel button on running active screen")
    cancel_btn = appium_driver_helper.get_element(appium_driver, "Cancel")
    cancel_btn.click()
    
    # Check for cancel popup 
    bart.step("Check I am on cancel menu")
    appium_driver_helper.get_element(appium_driver, "button-back")
    appium_driver_helper.get_element(appium_driver, "Back")
    confirm_btn = appium_driver_helper.get_element(appium_driver, "Confirm")
    confirm_btn.click()

    # Check 'X' Cycle cancelled popups appears
    bart.step("Check for 'X' cancel confirmation popup")
    appium_driver_helper.get_element(appium_driver, "popup-Cycle-cancelled")

    # Wait for a few seconds
    bart.step("Wait for machine to process")
    sleep(3)

    # Check I am back on the Material setting scrren
    appium_driver_helper.get_element(appium_driver, "button-save")
    appium_driver_helper.get_element(appium_driver, "button-delay")
    appium_driver_helper.get_element(appium_driver, "button-start")



@bart.scenario("Click back and get cancle cycle alert")
def test_cancel_alert(appium_driver):
    """Clicking back button on the cancel cycle alert should not cancel cycle"""

    # Place in logic from running.py

    # Verify I am on Running Cycle Screen
    bart.step("Check that I am on running cycle menu")
    # change to new resource_id
    appium_driver_helper.get_element(appium_driver, "Cancel")
    appium_driver_helper.get_element(appium_driver, "Options")

    # Click on the cancel button
    bart.step("Click back button on active screen")
    cancel_btn = appium_driver_helper.get_element(appium_driver, "Cancel")
    cancel_btn.click()

    # Check for cancel popup 
    bart.step("Check I am on cancel menu")
    appium_driver_helper.get_element(appium_driver, "button-back")
    back_btn = appium_driver_helper.get_element(appium_driver, "Back")
    appium_driver_helper.get_element(appium_driver, "Confirm")

    # Click on the cancel cycle button
    bart.step("Click cancel button on cancel menu")
    back_btn.click()

    # Verify I am on back on Running Cycle Screen
    bart.step("Check that I am back on running cycle screen")
    appium_driver_helper.get_element(appium_driver, "Cancel")
    appium_driver_helper.get_element(appium_driver, "Options")
