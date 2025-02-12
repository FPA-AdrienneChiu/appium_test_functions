import fpabart as bart
import modules.appium_driver.appium_driver_helper as appium_driver_helper
from time import sleep
import random

@bart.scenario("Checks an Alert appears when Dry Cycle complete")
def test_end_alert(appium_driver):
    """Finish alert appears when dry cycle is complete"""

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
 
    # Verify that I am near end of running cycle
    bart.step("Check I am on the running cycle page")
    sleep(3600)
 
    # Check that cycle complete menu popup
    bart.step("Check end cycle menu pops up")
    appium_driver_helper.get_element(appium_driver, "Add more time")
    appium_driver_helper.get_element(appium_driver, "Done")



@bart.scenario("Close complete alert with X button")
def test_end_XBtn(appium_driver):
    """Close dry cycle complete alert with X button"""

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

    #Click on Start button
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

    # Verify that I am near end of running cycle
    sleep(3600)

    # Check that end of cycle menu pops up
    bart.step("Check end cycle menu pop up")
    appium_driver_helper.get_element(appium_driver, "Add more time")
    appium_driver_helper.get_element(appium_driver, "Done")

    # Verify it goes back to material selection screen
    bart.step("Check I am back on material selection screen")
    dyer_title = appium_driver_helper.get_element(appium_driver, "title")

    dyer_title_text = appium_driver_helper.get_text(appium_driver, dyer_title)
    if dyer_title_text == "DRYER":
        print("Home screen title verification passed.")
    else:
        print("Home screen title verification failed.")



@bart.scenario("Close complete with Done button")
def test_end_Done(appium_driver):
    """Close dry cycle complete alert with done button"""

    # Logic for crease-free active needs to be put in
    
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

    # Select More options in material setting screen
    bart.step("Click on More options")
    appium_driver_helper.get_element(appium_driver, "More options").click()

    # Verify I am in More Options
    creaseFree_btn = appium_driver_helper.get_element(appium_driver, "Crease free")
    appium_driver_helper.get_element(appium_driver, "damp dry alert")
    creaseFree_btn.click()

    # Verify I am in Crease free menu and redirect back to material setting screen
    appium_driver_helper.get_element(appium_driver, "Off")
    appium_driver_helper.get_element(appium_driver, "On").click()
    appium_driver_helper.get_element(appium_driver, "Confirm").click()
    appium_driver_helper.get_element(appium_driver, "Done").click()

    #Redirect to settings page and Click on Start button
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

    # Verify that I am near end of running cycle
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
    """Cycle complete alert appears and click add more time"""

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

    #Click on Start button
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

    # Verify that I am near end of running cycle
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



@bart.scenario("Complete alert popsup again after add more time completed")
def test_end_alertComplete(appium_driver):
    """Cycle complete alert comes after dry cycle is completed again after adding more time"""

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

    #Click on Start button
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

    # Verify that I am near end of running cycle
    sleep(3600)

    # Check that cycle complete menu popup
    bart.step("Check end cycle menu pop up")
    addTime_btn = appium_driver_helper.get_element(appium_driver, "Add more time")
    appium_driver_helper.get_element(appium_driver, "Done")
    addTime_btn.click()

    # Check that it takes you back to time selection
    bart.step("Check redirect to time selection")
    sleep(1)
    appium_driver_helper.swipe(appium_driver, "0:30", "Auto", 1)
    appium_driver_helper.swipe(appium_driver, "0:40", "0:30", 1)
    appium_driver_helper.swipe(appium_driver, "0:50", "0:40", 1)
    time_option = ["0:30", "0:40", "0:50"] # add more times to swipe through

    # Select a random time
    bart.step(f"Selecting random time: {chosen_time}")
    chosen_time = random.choice(time_option)
    bart.step(f"Selecting random time: {chosen_time}")
    time_element = appium_driver_helper.get_element(appium_driver, chosen_time)
    time_element.click()
    sleep(3)

    # Click confirm for chosen time
    bart.step("Click confirm button")
    confirm_btn = appium_driver_helper.get_element(appium_driver, "Confirm")
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
