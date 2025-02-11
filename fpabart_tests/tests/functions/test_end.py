import fpabart as bart
import modules.appium_driver.appium_driver_helper as appium_driver_helper
from time import sleep
import random

@bart.scenario("Checks an Alert appears when Dry Cycle complete")
def test_end_alert(appium_driver):

    # Place in logic from running.py
 
    # Verify that I am near end of running cycle
    bart.step("Check I am on the running cycle page")
    appium_driver_helper.get_element(appium_driver, "cycle-time-remaning")
    appium_driver_helper.get_element(appium_driver, "button-cancel")
    appium_driver_helper.get_element(appium_driver, "button-options")
    sleep(3600)

    # Check that cycle complete menu popup
    bart.step("Check end cycle menu pops up")
    appium_driver_helper.get_element(appium_driver, "Add more time")
    appium_driver_helper.get_element(appium_driver, "Done")



@bart.scenario("Close complete alert with X button")
def test_end_XBtn(appium_driver):

    # Place in logic from running.py

    # Verify that I am near end of running cycle
    bart.step("Check I am on the running cycle page")
    appium_driver_helper.get_element(appium_driver, "cycle-time-remaning")
    appium_driver_helper.get_element(appium_driver, "button-cancel")
    appium_driver_helper.get_element(appium_driver, "button-options")
    sleep(3600)

    # Check that end of cycle menu pops up
    bart.step("Check end cycle menu pop up")
    appium_driver_helper.get_element(appium_driver, "Add more time")
    appium_driver_helper.get_element(appium_driver, "Done")

    # Verify it goes back to material selection page



@bart.scenario("Close complete with Done button")
def test_end_Done(appium_driver):

    # Logic for crease-free active
    
    # Verify that I am near end of running cycle
    bart.step("Check I am on the running cycle page")
    appium_driver_helper.get_element(appium_driver, "cycle-time-remaning")
    appium_driver_helper.get_element(appium_driver, "button-cancel")
    appium_driver_helper.get_element(appium_driver, "button-options")
    sleep(3600)

    # Check that end of cycle menu pops up
    bart.step("Check end cycle menu pop up")
    appium_driver_helper.get_element(appium_driver, "Add more time")
    done_btn = appium_driver_helper.get_element(appium_driver, "Done")
    done_btn.click()

    # Verify it goes back to material selection page
    bart.step("Check for screen title")
    dyer_title = appium_driver_helper.get_element(appium_driver, "title")

    dyer_title_text = appium_driver_helper.get_text(appium_driver, dyer_title)
    if dyer_title_text == "DRYER":
        print("Home screen title verification passed.")
    else:
        print("Home screen title verification failed.")



@bart.scenario("Close complete and add more time")
def test_end_addTime(appium_driver):

    # Place in logic from running.py

    # Verify that I am near end of running cycle
    bart.step("Check I am on the running cycle page")
    appium_driver_helper.get_element(appium_driver, "cycle-time-remaning")
    appium_driver_helper.get_element(appium_driver, "button-cancel")
    appium_driver_helper.get_element(appium_driver, "button-options")
    sleep(3600)

    # Check that cycle complete menu popup
    bart.step("Check end cycle menu pop up")
    addTime_btn = appium_driver_helper.get_element(appium_driver, "Add more time")
    appium_driver_helper.get_element(appium_driver, "Done")
    addTime_btn.click()

    # Check that it takes you back to time selection and confirm
    bart.step("Check redirect to time selection and click confirm")
    confirm_btn = appium_driver_helper.get_element(appium_driver, "Confirm")
    # logic for time selection
    confirm_btn.click()

    # Check that dry cycle continues with new set time
    bart.step("Cycle continues with new selected time")
    appium_driver_helper.get_element(appium_driver, "cycle-time-remaning")



@bart.scenario("Complete alert popsup after add more time completed")
def test_end_alertComplete(appium_driver):

    # Verify that I am near end of running cycle
    bart.step("Check I am on the running cycle page")
    appium_driver_helper.get_element(appium_driver, "cycle-time-remaning")
    appium_driver_helper.get_element(appium_driver, "button-cancel")
    appium_driver_helper.get_element(appium_driver, "button-options")
    sleep(3600)

    # Check that cycle complete menu popup
    bart.step("Check end cycle menu pop up")
    addTime_btn = appium_driver_helper.get_element(appium_driver, "Add more time")
    appium_driver_helper.get_element(appium_driver, "Done")
    addTime_btn.click()

    # Check that it takes you back to time selection and confirm
    bart.step("Check redirect to time selection and click confirm")
    confirm_btn = appium_driver_helper.get_element(appium_driver, "Confirm")
    # logic for time selection
    confirm_btn.click()

    # Check that dry cycle continues with new set time
    bart.step("Cycle continues with new selected time")
    appium_driver_helper.get_element(appium_driver, "cycle-time-remaning")


    # Wait for cycle to near complete
    sleep(3600)

    # Check that cycle complete menu popups the second time
    bart.step("Check end cycle menu popsup second time")
    addTime_btn = appium_driver_helper.get_element(appium_driver, "Add more time")
    appium_driver_helper.get_element(appium_driver, "Done")
