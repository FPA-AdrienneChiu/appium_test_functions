import fpabart as bart
import modules.appium_driver.appium_driver_helper as appium_driver_helper
from time import sleep
import random
from PythonCommsBusHijack.erd_lib import ERDLib
from PythonCommsBusHijack.ipb_control import IPB_Control
from high_spec_dryer_control import HD_control  # Import HD_control class


# Testing out capTouch

@bart.scenario("Running Auto")
def test_running_auto(appium_driver):
    """Test dryer's auto run cycle and verify UI elements"""

    # Check that I am on Home Screen
    bart.step("Check for screen title")
    dryer_title = appium_driver_helper.get_element(appium_driver, "title")

    dryer_title_text = appium_driver_helper.get_text(appium_driver, dryer_title)
    if dryer_title_text == "DRYER":
        print("Home screen title verification passed.")
    else:
        print("Home screen title verification failed.")

    # Check for material options and click one
    bart.step("Check that all materials are present")
    material_options = ["Mixed", "Cotton", "Polyester", "Silk", "Elastane", "Linen", "Down"]
    sleep(1)
    appium_driver_helper.swipe(appium_driver, "Down", "Mixed", 2)
    material_options = ["Acrylic", "Viscose", "Lyocell", "Hemp", "Ramie", "Nylon"]
    chosen_material = random.choice(material_options)

    bart.step(f"Selecting random material: {chosen_material}")
    material_element = appium_driver_helper.get_element(appium_driver, chosen_material)
    material_element.click()
    sleep(3)

    # Verify that the time is set to "AUTO"
    bart.step("Check if time is set to Auto")
    auto = appium_driver_helper.get_element(appium_driver, "Auto")
    appium_driver_helper.get_text(appium_driver, auto)

    time_selection = appium_driver_helper.get_element(appium_driver, "time")
    appium_driver_helper.get_text(appium_driver, time_selection)

    # Click on Start button
    bart.step("Click start")
    start_btn = appium_driver_helper.get_element(appium_driver, "button-start")
    start_btn.click()

    # Verify CapTouch step
    bart.step("Use CapTouch to start and activate cycle")
    # captouch_driver_helper.activate_captouch()  # Activate CapTouch functionality

    # Send CapTouch command using HD_control class
    port = "COM_PORT"  # Replace "COM_PORT" with the actual COM port
    erd_lib = ERDLib()  # Initialize ERDLib
    dryer_control = HD_control(port, erd_lib)
    dryer_control.dryer_start_pause()

    # Verify I am on Running Cycle Screen
    bart.step("Check that I am on running cycle menu")
    appium_driver_helper.get_element(appium_driver, "cycle-time-remaining")
    appium_driver_helper.get_element(appium_driver, "button-cancel")
    appium_driver_helper.get_element(appium_driver, "button-options")

    # Display current cycle state
    bart.step("Check for current cycle state")
    cycle_status = ["Fill", "Wash", "Rinse", "Spin", "Dry", "Cooling", "Load sensing", "Steam"]
    sleep(3)
    appium_driver_helper.get_element(appium_driver, cycle_status)

    # Wait for 30 seconds of no interaction
    bart.step("Wait 30 secs to sleep")
    sleep(30)

    # Check footer and hamburger menu disappears
    bart.step("Hamburger and Footer Menu Disappears")
    menu_btns = ["Cancel", "Options", "Add item"]
    all_disappeared = True
    for element in menu_btns:
        try:
            appium_driver_helper.get_element(appium_driver, element, max_attempts=1)
            print(f"{element} did not disappear.")
            all_disappeared = False
        except RuntimeError:
            pass
    if all_disappeared:
        print("Footer and hamburger menu disappeared as expected.")

    bart.step("Complete Scenario")
    appium_driver.terminate_app("com.fisherpaykel.laundry.fcs200")
    sleep(2)
    appium_driver.activate_app("com.fisherpaykel.laundry.fcs200")