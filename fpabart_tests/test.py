import logging

from appium.options.android import UiAutomator2Options
from appium.webdriver import Remote
from appium.webdriver.appium_service import AppiumService


logging.basicConfig(
    level=logging.NOTSET,  # Capture all log levels.
    format="%(asctime)s - %(module)s - %(levelname)s - %(message)s",
    filename="WHY_WONT_APPIUM_WORK.log",
    filemode="w",
)
logger = logging.getLogger()

appium_address = "127.0.0.1"
appium_port = 4723
print("1")

service = AppiumService()
print("2")
service.start(args=["--address", appium_address, "-p", str(appium_port)], timeout_ms=20000)
print("3")

capabilities = {
    "platformName": "Android",
    "platformVersion": "11",
    "deviceName": "i350fisher_paykel ",
    "appPackage": "com.fisherpaykel.laundry.fcs200",
    "appActivity": "com.fisherpaykel.laundry.fcs200.MainActivity",
    "automationName": "UiAutomator2",
    "noReset": "true",
    "fullReset": "false",
}
print("4")

options = UiAutomator2Options().load_capabilities(capabilities)
print("5")
driver = Remote(f"http://{appium_address}:{appium_port}", options=options)
print("6")
