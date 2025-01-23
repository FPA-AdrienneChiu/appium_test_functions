"""."""

import log_config
import logging
import Start

from result import Result
from time import sleep



import bart


@bart.scenario(
    "cycle_selection_dryer"
)
def test_cycle_selection_dryer1():
    
    bart.report("Here is some information at the top of the report.")
    # bart.report("You can add multiple lines.")
    bart.step("I am on the fibre selection screen of dryer")
    dryer = Start.find_element("DRYER")
    dryer_text = Start.get_text(dryer)[0]
    assert dryer_text == "DRYER"
        
        
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
    test_cycle_selection_dryer1()

    # Stop the Appium service after the test is done
    srvc.stop()
