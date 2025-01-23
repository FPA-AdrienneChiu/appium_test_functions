"""."""

import json

from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy as By
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.common.exceptions import NoSuchElementException
from PIL import ImageChops

APPIUM_PORT = 4723
APPIUM_HOST = "127.0.0.1"
driver = None


def appium_service():
    """Connect to the Appium server."""
    service = AppiumService()
    service.start(
        args=["--address", APPIUM_HOST, "-p", str(APPIUM_PORT)],
        timeout_ms=20000,
    )
    return service


# Function to create a new driver instance
capabilities = dict(
    platformName="Android",
    platformVersion="11",
    deviceName="i350fisher_paykel",
    appPackage="com.fisherpaykel.laundry.fcs200",
    appActivity="com.fisherpaykel.laundry.fcs200.MainActivity",
    automationName="uiautomator2",
    noReset="true",
    fullReset="false",
)


def init_global_driver():
    """."""
    global driver
    print("##### Creating driver")
    appium_host = f"http://{APPIUM_HOST}:{APPIUM_PORT}"

    with open("capabilities.json", "r") as file:
        appium_options = UiAutomator2Options().load_capabilities(json.load(file))

    driver = webdriver.Remote(appium_host, options=appium_options)


def search_modes(identifier: str):
    """Return a list of search modes.

    The listed modes are:
    - resource-id
    - accessibility-id
    - id
    - content-desc
    """
    return [
        (By.XPATH, f'//*[@resource-id="{identifier}"]'),
        (By.ACCESSIBILITY_ID, identifier),
        (By.ID, identifier),
        (By.XPATH, f"//*[@content-desc={identifier}]"),
    ]


def wait_for(identifier: str):
    """Wait until an element with the given identifier is visible.

    Uses the search modes above defined in `search_modes(...)
    Returns True if the element is found, False otherwise.
    """
    for by, locator in search_modes(identifier):
        if wait_for_by(by, locator):
            return True
    return False


def wait_for_by(by, identifier):
    """Support function for `wait_for()`.

    Halts / waits until an element with the given identifier is visible
    Returns True if the element is found, False otherwise.
    """
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.presence_of_all_elements_located((by, identifier)))
        return True
    except Exception as e:
        print(e)
    return False


def find_element(identifier: str):
    """Find an element with the given identifier.

    It tries different search modes until the element is found.
    It returns the found element, or None if no element is found.
    """
    print("Find element:", identifier, "...")

    element = None
    for by, locator in search_modes(identifier):
        if wait_for_by(by, locator):
            element = find_element_by(by, locator)
            if element is not None:
                break

    if element is None:
        print("Failed to find:", identifier)
    else:
        print("SUCCESS, found: ", identifier)

    return element


def find_element_by(by, identifier):
    """Support function for `find_element()`.

    Returns the element if found, None otherwise.
    """
    element = None
    try:
        element = driver.find_element(by, value=identifier)
    except NoSuchElementException:
        print("ERROR: NoSuchElementException", identifier)
    except Exception as e:
        print(e)
        print(f"ERROR: {e}", identifier)
    return element


MAX_DEPTH = 5


def get_text(element, depth=MAX_DEPTH):
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
        text = element.get_attribute("content-desc")
        if text not in [None, "", "null"]:
            texts.append(text)
    except Exception as e:
        print(f"Error retrieving text: {e}")

    # Find child elements
    try:
        children = element.find_elements(By.XPATH, ".//*/child::*")
        for child in children:
            child_texts = get_text(child, depth - 1)
            texts.extend(child_texts)  # Append texts from children
    except Exception as e:
        print(f"Error finding children: {e}")

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
            except Exception as e:
                print(e)
        for attr in attributes:
            try:
                data[attr] = element.get_attribute(attr)
            except Exception as e:
                print(e)

    except Exception as e:
        print(f"Error while accessing element: {e}")

    return data


def swipe(start_location_ID, end_location_ID, repetitions):
    """Perform a swipe action from a start element to an end element, a specified number of times."""
    start_location = find_element(start_location_ID).location
    end_location = find_element(end_location_ID).location

    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(
        driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
    )
    for i in range(repetitions):
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


def verify_element_text(identifier: str, expected_text: str):
    """."""
    try:
        element = driver.find_element(By.ID, identifier)
        actual_text = element.get_attribute("text")
        if actual_text == expected_text:
            print(f"Text verification passed: {actual_text}")
        else:
            print(
                f"Text verification failed: expected '{expected_text}', but got '{actual_text}'"
            )
    except Exception as e:
        print(f"Error: {e}")


# Function to compare images
def compare_images(img1, img2):
    diff = ImageChops.difference(img1, img2)
    return not diff.getbbox()
