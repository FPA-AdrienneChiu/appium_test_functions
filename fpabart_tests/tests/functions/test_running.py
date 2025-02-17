import fpabart as bart
import modules.appium_driver.appium_driver_helper as appium_driver_helper
from time import sleep
import random


@bart.scenario("Running Auto")
def test_running_auto(appium_driver):
    """Test dryers auto run cycle and verify UI elements"""

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
    material_options =  ["Mixed", "Cotton", "Polyester", "Wool", "Silk", "Elastane", "Linen", "Down",] # Wool and cashmere does not have auto
    sleep(1)
    appium_driver_helper.swipe(appium_driver, "Down", "Mixed", 2)
    material_options = ["Cashmere", "Acrylic", "Viscose", "Lyocell",  "Hemp", "Ramie", "Nylon"]
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

    # Click on Start button
    bart.step("Click start")
    start_btn = appium_driver_helper.get_element(appium_driver, "button-start") 
    start_btn.click()

    # Verify Captouch step
    # bart.step("Use captouch to start and activate cycle")
    
    # Verify I am on Running Cycle Screen
    bart.step("Check that I am on running cycle menu")
    appium_driver_helper.get_element(appium_driver, "cycle-time-remaning")
    appium_driver_helper.get_element(appium_driver, "button-cancel")
    appium_driver_helper.get_element(appium_driver, "button-options")

    # Displays current cycle state
    bart.step("Checks for current cycle state")
    cycle_status = ["Fill", "Wash", "Rinse", "Spin", "Dry", "Cooling"," Load sensing", "Steam"]
    sleep(3)
    appium_driver_helper.get_element(appium_driver, cycle_status)

    # Wait for 30 seconds of no interaction
    bart.step("Wait 30 secs to sleep")
    sleep(30)

    # Check footer and hamburger menu dissapears
    bart.step("Hamburger and Footer Menu Dissapears") 
    menu_btns = ["Cancel", "Options", "Add item"] # Create list of elements
    all_disappeared = True # Set to true all elements are gone
    for element in menu_btns:
        try:
            appium_driver_helper.get_element(appium_driver, element, max_attempts=1) # Search for elements, allow one try
            print(f"{element} did not disappear.")
            all_disappeared = False # Returns false if any listed elements are found 
        except RuntimeError:
            pass # All elements dissapeared
    if all_disappeared:
        print("Footer and hamburger menu disappeared as expected.") 

    bart.step("Complete Scenario")
    appium_driver.terminate_app("com.fisherpaykel.laundry.fcs200")
    sleep(2)  # Wait for a couple of seconds.
    appium_driver.activate_app("com.fisherpaykel.laundry.fcs200")




@bart.scenario("Running Timed")
def test_running_time(appium_driver):
    """Test dryers timed run cycle and verify UI elements"""

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
    material_options =  ["Mixed", "Cotton", "Polyester", "Wool", "Silk", "Elastane", "Linen", "Down",] # Wool and cashmere does not have auto
    sleep(1)
    appium_driver_helper.swipe(appium_driver, "Down", "Mixed", 2)
    material_options = ["Cashmere", "Acrylic", "Viscose", "Lyocell",  "Hemp", "Ramie", "Nylon"]
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
    Auto.click()

    # Verify that all time options are available
    bart.step("Swipe through all time options")
    sleep(1)
    appium_driver_helper.swipe(appium_driver, "0:30", "Auto", 1)
    appium_driver_helper.swipe(appium_driver, "0:40", "0:30", 1)
    appium_driver_helper.swipe(appium_driver, "0:50", "0:40", 1)

    time_option = ["0:30", "0:40", "0:50"] # add more times to swipe through

    chosen_time = random.choice(time_option)

    bart.step(f"Selecting random time: {chosen_time}")
    time_element = appium_driver_helper.get_element(appium_driver, chosen_time)
    time_element.click()
    sleep(3)

    # Click Confirm to return to settings page
    bart.step("Click on confirm for chosen time option")
    Confirm = appium_driver_helper.get_element(appium_driver, "button-confirm" )
    Confirm.click()

    # Click on Start button
    bart.step("Click start")
    start_btn = appium_driver_helper.get_element(appium_driver, "Start") 
    start_btn.click()

    # Verify Captouch step
    # bart.step("Use captouch to start and activate cycle")

    # Verify Chosen Time is displayed on the running screen
    bart.step("Verify that the chosen time is displayed on running screen")
    appium_driver_helper.get_element(appium_driver, "cycle-time-remaning")

    # Displays current cycle state
    bart.step("Checks for current cycle state")
    cycle_status = ["Fill", "Wash", "Rinse", "Spin", "Dry", "Cooling"," Load sensing", "Steam"]
    sleep(3)
    appium_driver_helper.get_element(appium_driver, cycle_status)
    
    # Wait for 30 seconds of no interaction
    bart.step("Wait 30 secs to sleep")
    sleep(30)

    # Check footer and hamburger menu dissapears
    bart.step("Hamburger and Footer Menu Dissapears") 
    menu_btns = ["Cancel", "Options", "Add item"] # Create list of elements
    all_disappeared = True # Set to true all elements are gone
    for element in menu_btns:
        try:
            appium_driver_helper.get_element(appium_driver, element, max_attempts=1) # Search for elements, allow one try
            print(f"{element} did not disappear.")
            all_disappeared = False # Returns false if any listed elements are found 
        except RuntimeError:
            pass # All elements dissapeared
    if all_disappeared:
        print("Footer and hamburger menu disappeared as expected.")


