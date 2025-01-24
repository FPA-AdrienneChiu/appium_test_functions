"""Provide helper functions for Appium-based activities.

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

from appium.webdriver import Remote
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException,  InvalidSelectorException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

from time import sleep


logger = logging.getLogger(__name__)


def _get_search_modes(element_id: str) -> list:
    """Get a list of search modes for the provided element ID.

    Args:
        element_id (str): The element's ID.

    Returns:
        list: A list of search modes for the provided element ID.
    """
    search_modes = [
        (AppiumBy.XPATH, f'//*[@resource-id="{element_id}"]'),
        (AppiumBy.ACCESSIBILITY_ID, element_id),
        (AppiumBy.ID, element_id),
        (AppiumBy.XPATH, f'//*[@content-desc="{element_id}"]'),
    ]

    for search_mode in search_modes:
        logger.debug(f"Search mode for '{element_id}': {search_mode}")

    return search_modes


def get_element(appium_driver: Remote, element_id: str, max_attempts: int = 5) -> WebElement:
    """Wait for an element to appear on the UI and return the element.

    Args:
        appium_driver (Remote): The Appium driver.
        element_id (str): The element's ID.
        max_attempts (int): The maximum number of times to search for the element. Each attempt takes approximately
            2 seconds. Defau it was found, or 'None' if it was not.
    """
    logger.info(f"Looking for element '{element_id}'...")
    element = None
    wait = WebDriverWait(appium_driver, timeout=0.5, poll_frequency=0.5)

    for attempt_index in range(max_attempts):
        logger.debug(f"Searching for element '{element_id}. Attempt {attempt_index + 1}/{max_attempts}")

        for search_mode, locator in _get_search_modes(element_id):
            try:
                logger.debug(f"Waiting for locator '{locator}' with search mode '{search_mode}'...")
                wait.until(expected_conditions.presence_of_all_elements_located((search_mode, locator)))
                logger.info(f"Found element '{element_id}' with search mode '{search_mode}' and locator '{locator}'!")

                element = appium_driver.find_element(search_mode, value=locator)

                break

            except TimeoutException:
                logger.warning(
                    f"Timed out looking for element '{element_id}' with search mode "
                    f"{search_mode}' and locator'{locator}'!"
                )

        if element is not None:
            break

    if element is None:
        raise RuntimeError(f"Could not find element '{element_id}' after {max_attempts} attempts!")

    return element


def restart_app(appium_driver: Remote):
    """Restart the UI application.

    Args:
        appium_driver (Remote): The Appium driver.
    """
    appium_driver.terminate_app("com.fpa.cook_ui_cavity_flutter")
    sleep(2)  # Wait for a couple of seconds.
    appium_driver.activate_app("com.fpa.cook_ui_cavity_flutter")


MAX_DEPTH = 5


def get_text(appium_driver, element, depth=MAX_DEPTH):
    """Retrieve the "innerText" of a provided element.

    It will also retrieve text from children elements.
    It returns a list of texts [string].
    """
    if depth < 0:
        return []  # Return an empty list if maximum depth is exceeded
    if element is None:
        return []

    texts = []

    try:
        # Retrieve the content description text
        text = element.get_attribute(appium_driver, "content-desc")
        if text not in [None, "", "null"]:
            texts.append(text)
    except TypeError as e:
        print(f"Error retrieving text: {e}")
    except AttributeError as e:
        print(f"Error retrieving text: {e}")
    except ValueError as e:
        print(f"Error retrieving text: {e}")

    # Find child elements

    try:
        children = element.get_element(appium_driver, AppiumBy.XPATH, ".//*/child::*")
        for child in children:
            child_texts = get_text(child, depth - 1)
            texts.extend(child_texts)  # Append texts from children
    except TypeError as e:
        print(f"Error retrieving text: {e}")
    except AttributeError as e:
        print(f"Error retrieving text: {e}")
    except ValueError as e:
        print(f"Error retrieving text: {e}")

    return texts


def get_attributes(element):
    """Extract the attributes of a given element.

    It returns a dictionary of attributes.
    """
    if element is None:
        return {}

    attrs = ["location", "tag_name", "size"]
    # 'text', 'rect'
    attributes = [
        "package",
        "class",
        "content-desc",
        "resource-id",
        "enabled",
        "checkable",
        "checked",
        "clickable",
        "focusable",
        "focused",
        "long-clickable",
        "scrollable",
        "selected",
        "displayed",
    ]
    # 'password', 'bounds'

    data = {}
    try:
        for a in attrs:
            try:
                if hasattr(element, a):
                    data[a] = getattr(element, a)
            except TypeError as e:
                print(f"Error while accessing element: {e}")
            except AttributeError as e:
                print(f"Error while accessing element: {e}")
            except ValueError as e:
                print(f"Error while accessing element: {e}")
        for attr in attributes:
            try:
                data[attr] = element.get_attribute(attr)
            except TypeError as e:
                print(f"Error while accessing element: {e}")
            except AttributeError as e:
                print(f"Error while accessing element: {e}")
            except ValueError as e:
                print(f"Error while accessing element: {e}")

    except TypeError as e:
        print(f"Error while accessing element: {e}")
    except AttributeError as e:
        print(f"Error while accessing element: {e}")
    except ValueError as e:
        print(f"Error while accessing element: {e}")

    return data


def swipe(appium_driver, start_location_id, end_location_id, repetitions):
    """Perform a swipe action from a start element to an end element, a specified number of times."""
    start_location = get_element(appium_driver, start_location_id).location
    end_location = get_element(appium_driver, end_location_id).location

    actions = ActionChains(appium_driver)
    actions.w3c_actions = ActionBuilder(
        appium_driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
    )
    for _i in range(repetitions):
        actions.w3c_actions.pointer_action.move_to_location(
            start_location["x"], start_location["y"]
        )  # go to 9
        actions.w3c_actions.pointer_action.click_and_hold()
        actions.w3c_actions.pointer_action.move_to_location(
            end_location["x"], end_location["y"]
        )  # go to center
        actions.w3c_actions.pointer_action.pause(0.3)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


def verify_text(appium_driver, element_id: str, expected_text: str):
    """."""
    element = get_element(appium_driver, element_id)
    if element:
        actual_text = get_text(appium_driver, element)
        if actual_text == expected_text:
            print(f"The text '{expected_text}' is present and correct")
        else:
            print(f"The text '{expected_text}' is not present or correct")
        return actual_text == expected_text
    return False


def find_element(appium_driver, element_id):
    """Get the WebElement by ID."""
    try:
        element = WebDriverWait(appium_driver, 10).until(
            expected_conditions.presence_of_element_located((AppiumBy.ID, element_id))
        )
        print(f"Element found with ID: {element_id} - Type: {type(element)}")
        return element
    except (TimeoutException, InvalidSelectorException) as e:
        print(f"Error finding element with ID: {element_id}, Error: {e}")
        raise


def is_focused(element):
    """Check if the 'selected' attribute of the element is true or false."""
    if not isinstance(element, WebElement):
        raise ValueError("Invalid argument: 'element' must be a WebElement, not a different type.")
    checked_value = element.get_attribute("selected")
    return checked_value.lower() == "true" if checked_value else False


def click_correct_button(off_button, on_button):
    """."""
    off_focused = is_focused(off_button)
    on_focused = is_focused(on_button)

    # Determine which button is focused and click on it.
    if off_focused:
        on_button.click()
        print("Clicked on the Off button")
    elif on_focused:
        off_button.click()
        print("Click on the ON button")
    else:
        print("Test Failed")


def ensure_button_selected(element):
    """Ensure the button is selected; if not selected, click it to select."""
    if not isinstance(element, WebElement):
        raise ValueError("Invalid argument: 'element' must be a WebElement, not a different type.")
    if is_focused(element):
        print("Button is already selected.")
    else:
        element.click()
        print("Button was not selected; now it is selected.")
