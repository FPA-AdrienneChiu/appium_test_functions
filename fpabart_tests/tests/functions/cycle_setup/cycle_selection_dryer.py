"""."""

import log_config
import logging
import Start

from result import Result
from time import sleep


logger = logging.getLogger(log_config.get_hierarchical_logger_name(__name__))
logger.feature("CYCLE SETUP")


def cycle_selection_dryer():
    """."""
    logger.scenario("cycle_selection_dryer")


    logger.step("I am on the fibre selection screen of dryer")
    dryer = Start.find_element("DRYER")
    dryer_text = Start.get_text(dryer)[0]
    if dryer_text == "DRYER" :
        logger.result(Result.PASS)
    else:
        logger.result(Result.FAIL)


    logger.step("I check if all fabric options are available")
    # List of fabric options before swipe
    fabrics_before_swipe = ["Mixed", "Polyester", "Cotton", "Elastane", "Silk", "Wool"]
    # Find elements before swipe
    fabric_elements = {fabric: Start.find_element(fabric) for fabric in fabrics_before_swipe}
    # Perform swipe action
    Start.swipe("Silk", "Mixed", 2)
    # List of fabric options after swipe
    fabrics_after_swipe = ["Acrylic", "Viscose", "Linen", "Lyocell", "Down", "Hemp", "Cashmere", "Ramie", "Nylon"]
    # Find elements after swipe
    fabric_elements.update({fabric: Start.find_element(fabric) for fabric in fabrics_after_swipe})
    # Check if any fabric option is None
    if any(element is None for element in fabric_elements.values()):
      logger.result(Result.FAIL)
    else:
      logger.result(Result.PASS)
      
      
    
        
        
    fabric_options_before_swipe = [ "Mixed", "Cotton", "Polyester", "Elastane", "Acrylic", "Viscose" , "Silk"]
    # fabric_options_before_swipe = [ "Mixed"]
    fabric_options_after_swipe = ["Linen", "Lyocell", "Down", "Hemp", "Ramie"]

# Click on fabric options before swipe
    for fabric in fabric_options_before_swipe:
     logger.step(f"I click on {fabric} fabric option")
     fabric_element = Start.find_element(fabric)
     fabric_element.click()
     fabric_header = Start.find_element(fabric.upper())
     if fabric_header is None:
        logger.result(Result.FAIL)
     else:
        logger.result(Result.PASS)

     logger.step("I check the default time and click on start option")
     default_time_card = Start.find_element("option-card-time")
     default_time = Start.get_text(default_time_card)[1]
     
     
     
     start_cycle = Start.find_element("Start")
     start_cycle.click()

     logger.step("I verify that the selected fabric and time is correctly displayed on the cycle progress screen")
     start_header = Start.find_element(fabric.upper())
     start_header_text = Start.get_text(start_header)[0]
     selected_time = Start.find_element("cycle-time-remaning")
     if selected_time is not None:
       selected_time_text = Start.get_text(selected_time)[0]
       if start_header_text == fabric.upper() and selected_time_text == default_time:
        logger.result(Result.PASS)
       else:
        logger.result(Result.FAIL)
       selected_time.click()
     else:
       logger.result(Result.FAIL)
       logger.step("Auto element not found, continuing to next step")

     logger.step("I return to the fabric selection screen")
     start_header.click()
     cancel_cycle = Start.find_element("Cancel")
     cancel_cycle.click()
     if dryer_text == "DRYER":
      logger.result(Result.PASS)
     else:
      logger.result(Result.FAIL)

   # Swipe to reveal additional fabric options
    Start.swipe("Silk", "Mixed", 3)

   # Click on fabric options after swipe
    for fabric in fabric_options_after_swipe:
     logger.step(f"I click on {fabric} fabric option")
     fabric_element = Start.find_element(fabric)
     fabric_element.click()
     fabric_header = Start.find_element(fabric.upper())
     if fabric_header is None:
        logger.result(Result.FAIL)
     else:
        logger.result(Result.PASS)

     logger.step("I check the default time and click on start option")
     default_time_card = Start.find_element("option-card-time")
     default_time = Start.get_text(default_time_card)[1]
     
     start_cycle = Start.find_element("Start")
     start_cycle.click()

     logger.step("I verify that the selected fabric and time is correctly displayed on the cycle progress screen")
     start_header = Start.find_element(fabric.upper())
     start_header_text = Start.get_text(start_header)[0]
     selected_time = Start.find_element("cycle-time-remaning")
     if selected_time is not None:
       selected_time_text = Start.get_text(selected_time)[0]
       if start_header_text == fabric.upper() and selected_time_text == default_time:
        logger.result(Result.PASS)
       else:
        logger.result(Result.FAIL)
       selected_time.click()
     else:
       logger.result(Result.FAIL)
       logger.step("Auto element not found, continuing to next step")

     logger.step("I return to the fabric selection screen")
     start_header.click()
     cancel_cycle = Start.find_element("Cancel")
     cancel_cycle.click()
     print(dryer_text)
     if dryer_text == "DRYER":
      logger.result(Result.PASS)
     else:
      logger.result(Result.FAIL)
      
      

# press start popup to be added once available
#final screen once cycle starts to be added
# i icon on each fabric to be added
#i icon above estimates
    
        

  

# main starts here
if __name__ == "__main__":
    """
    This is the main entry point of the script.
    It creates a driver, starts the Appium service
    runs the test, and then stops the service.
    """
    # Launch the model

    # global driver
    Start.init_global_driver()

    # Start the Appium service
    srvc = Start.appium_service()

    # Run the test
    cycle_selection_dryer()

    # Stop the Appium service after the test is done
    srvc.stop()
