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
    e = Start.find_element("DRYE")
    if e is None :
        logger.result(Result.FAIL)
    else:
        logger.result(Result.PASS)
        
    
    
    logger.step("Move the menu along ")
    Start.swipe("Silk", "Mixed", 2)
    logger.result(Result.PASS)
    
    logger.step("When I tap on the Acrylic fabric option")
    acrylic = Start.find_element("Acrylic")
    acrylic.click()
    logger.result(Result.PASS)
    
    
    
    
    
# main starts here
if __name__ == "__main__":
    """
    This is the main entry point of the script.
    It creates a driver, starts the Appium service
    runs the test, and then stops the service.
    """
    # Lanunch the model

    # global driver
    Start.init_global_driver()

    # Start the Appium service
    srvc = Start.appium_service()

    # Run the test
    cycle_selection_dryer()

    # Stop the Appium service after the test is done
    srvc.stop()