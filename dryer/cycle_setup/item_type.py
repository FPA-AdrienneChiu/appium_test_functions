"""."""

import log_config
import logging
import Start

from result import Result
from time import sleep


logger = logging.getLogger(log_config.get_hierarchical_logger_name(__name__))
logger.feature("CYCLE SETUP")


def item_type():
    """."""
    logger.scenario("item type")


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
      