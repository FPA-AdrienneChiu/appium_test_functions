"""Test fixtures for use in the BART testing system.

&copy; Copyright 2024, Fisher & Paykel Appliances Ltd

All rights reserved. Fisher & Paykel's source code is an
unpublished work and the use of a copyright notice does not imply otherwise.
This source code contains confidential, trade secret material of
Fisher & Paykel Appliances Ltd.
Any attempt or participation in deciphering, decoding, reverse engineering
or in any way altering the source code is strictly prohibited,
unless the prior written consent of Fisher & Paykel is obtained.
Permission to use, copy, publish, modify and distribute for any purpose
is not permitted without specific, written prior permission from
Fisher & Paykel Appliances Limited.
"""

import logging
import pytest

from appium.options.android import UiAutomator2Options
from appium.webdriver import Remote
from appium.webdriver.appium_service import AppiumService


logger = logging.getLogger(__name__)

_appium_driver = None


@pytest.fixture
def appium_driver() -> Remote:
    """Create the Appium driver.

    Returns:
        Remote: The Appium driver.
    """
    global _appium_driver

    if _appium_driver is None:
        appium_address = "127.0.0.1"
        appium_port = 4723

        # Start the Appium server before we create the Appium driver.
        logger.debug(f"Starting Appium service at {appium_address}:{appium_port}")
        service = AppiumService()
        service.start(args=["--address", appium_address, "-p", str(appium_port)], timeout_ms=20000)

        capabilities = {
            "platformName": "Android",
            "appium:platformVersion": "11",
            "appium:deviceName": "i350fisher_paykel ",
            "appium:appPackage": "com.fisherpaykel.laundry.fcs200",
            "appium:appActivity": "com.fisherpaykel.laundry.fcs200.MainActivity",
            "appium:automationName": "uiautomator2",
            "appium:noReset": "true",
            "appium:fullReset": "false"
        }

        logger.debug(f"Loading capabilities: {capabilities}")
        options = UiAutomator2Options().load_capabilities(capabilities)
        logger.debug(f"Creating Appium driver at http://{appium_address}:{appium_port}")
        driver = Remote(f"http://{appium_address}:{appium_port}", options=options)

        logger.info("Successfully set up Appium!")
        _appium_driver = driver

    return _appium_driver
