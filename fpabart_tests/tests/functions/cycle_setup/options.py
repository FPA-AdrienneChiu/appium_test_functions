"""."""

import log_config
import logging
import Start

from result import Result
from time import sleep


logger = logging.getLogger(log_config.get_hierarchical_logger_name(__name__))
logger.feature("CYCLE SETUP")


def options():
    """."""
    logger.scenario("options")


    logger.step("I am on the fibre selection screen of dryer")
    dryer = Start.find_element("DRYER")
    dryer_text = Start.get_text(dryer)[0]
    if dryer_text == "DRYER" :
        logger.result(Result.PASS)
    else:
        logger.result(Result.FAIL)
      
      
    logger.step("I click on Mixed fabric option")
    Mixed = Start.find_element("Mixed")
    Mixed.click()
    Mixed_header = Start.find_element("MIXED")
    Mixed_header_text = Start.get_text(Mixed_header)[0]
    if Mixed_header_text == "MIXED":
          logger.result(Result.PASS)
    else:
        logger.result(Result.FAIL)
      
    logger.step("I verify item type option and default value")
    item_type_dryer = Start.find_element("option-card-item-type")
    item_type_title =Start.get_text(item_type_dryer)[0]
    item_type_default = Start.get_text(item_type_dryer)[1]
    # print(item_type_title)
    # print(item_type_default)
    if item_type_title == "Item type" and item_type_default == "Moderate":
      logger.result(Result.PASS)
    else:
      logger.result(Result.FAIL)
      
    logger.step("I verify dryness level option and default value")
    dryness_level = Start.find_element("option-card-dryness level")
    dryness_level_title =Start.get_text(dryness_level)[0]
    dryness_level_default = Start.get_text(dryness_level)[1]
    if dryness_level_title == "dryness level" and dryness_level_default == "dry":
      logger.result(Result.PASS)
    else:
      logger.result(Result.FAIL)
      
      
    logger.step("I verify rack dry option and default value")
    rack_dry = Start.find_element("option-card-rack dry")
    rack_dry_title =Start.get_text(rack_dry)[0]
    rack_dry_default = Start.get_text(rack_dry)[1]
    if rack_dry_title == "rack dry" and rack_dry_default == "Off":
      logger.result(Result.PASS)
    else:
      logger.result(Result.FAIL)
      
    
    logger.step("I verify treatment option and default value")
    treatment = Start.find_element("option-card-Treatment")
    treatment_title =Start.get_text(treatment)[0]
    treatment_default = Start.get_text(treatment)[1]
    if treatment_title == "Treatment" and treatment_default == "dry":
      logger.result(Result.PASS)
    else:
      logger.result(Result.FAIL)
      
      
    logger.step("I verify time option and default value")
    time = Start.find_element("option-card-time")
    time_title =Start.get_text(time)[0]
    time_default = Start.get_text(time)[1]
    if time_title == "time" and time_default == "Auto":
      logger.result(Result.PASS)
    else:
      logger.result(Result.FAIL)
      
      
    logger.step("I verify more options option")
    more_options = Start.find_element("option-card-More options")
    more_options_title =Start.get_text(more_options)[0]
    print(more_options_title)
    # time_default = Start.get_text(time)[1]
    if more_options_title == "More options":
      logger.result(Result.PASS)
    else:
      logger.result(Result.FAIL)
      
      
    logger.step("I verify estimated time and default value")
    estimate = Start.find_element("Estimate\n0:45 - 1:30")
    estimate_title =Start.get_text(estimate)
    print(estimate_title)
    # time_default = Start.get_text(time)[1]
    # if more_options_title == "More options":
    #   logger.result(Result.PASS)
    # else:
    #   logger.result(Result.FAIL)
      
    
      
      
      
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
    options()

    # Stop the Appium service after the test is done
    srvc.stop()
      
      
    