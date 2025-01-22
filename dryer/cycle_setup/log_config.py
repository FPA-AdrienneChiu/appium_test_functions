"""."""

import logging
import sys

from logging import LogRecord
from result import Result


PARENT_LOGGER_NAME = "parent_logger"

# Behaviour Driven Testing custom log levels.
FEATURE_LOG_LEVEL = 21
FEATURE_LOG_NAME = "FEATURE"
SCENARIO_LOG_LEVEL = 22
SCENARIO_LOG_NAME = "SCENARIO"
STEP_LOG_LEVEL = 23
STEP_LOG_NAME = "STEP"
RESULT_LOG_LEVEL = 24
RESULT_LOG_NAME = "RESULT"
REPORT_LOG_LEVEL = 25
REPORT_LOG_NAME = "REPORT"


class LogLevelFilter(logging.Filter):
    """Filter the logs to only record logs of certain levels."""

    def __init__(self, levels: list):
        """Create the filter and set the log levels to capture.

        Args:
            levels (list): The log levels for the filter to capture. The filter will ignore logs of all other levels.
        """
        self.levels = levels

    def filter(self, record: LogRecord) -> bool:
        """According to the filter, determine if the specified record should be logged.

        Args:
            record (LogRecord): The record to be (or not to be) logged.

        Returns:
            bool: True if the record should be logged or False if the record should not be logged.
        """
        return record.levelno in self.levels


def feature(self, message: str, *args: tuple, **kwargs: dict) -> None:
    """Log 'msg % args' with severity 'FEATURE'.

    Args:
        message (str): The message to log.
    """
    if self.isEnabledFor(FEATURE_LOG_LEVEL):
        self._log(FEATURE_LOG_LEVEL, message, args, **kwargs)


def scenario(self, message: str, *args: tuple, **kwargs: dict) -> None:
    """Log 'msg % args' with severity 'SCENARIO'.

    Args:
        message (str): The message to log.
    """
    if self.isEnabledFor(SCENARIO_LOG_LEVEL):
        self._log(SCENARIO_LOG_LEVEL, message, args, **kwargs)


def step(self, message: str, *args: tuple, **kwargs: dict) -> None:
    """Log 'msg % args' with severity 'STEP'.

    Args:
        message (str): The message to log.
    """
    if self.isEnabledFor(STEP_LOG_LEVEL):
        self._log(STEP_LOG_LEVEL, message, args, **kwargs)


def result(self, result: Result, *args: tuple, **kwargs: dict) -> None:
    """Log 'msg % args' with severity 'RESULT'.

    Args:
        result (Result): The result to log.
    """
    if self.isEnabledFor(RESULT_LOG_LEVEL):
        self._log(
            RESULT_LOG_LEVEL, result.value, args, **kwargs
        )  # 'result.value' gets the enumerated value's string.


def report(self, message: str, *args: tuple, **kwargs: dict) -> None:
    """Log 'msg % args' with severity 'REPORT'.

    Args:
        message (str): The message to log.
    """
    if self.isEnabledFor(REPORT_LOG_LEVEL):
        self._log(REPORT_LOG_LEVEL, message, args, **kwargs)


def get_hierarchical_logger_name(module_name: str) -> str:
    """Create a name for a child logger such that, when created, the child logger will inherit the parent logger's properties.

    Args:
        module_name (str): The name of the module for which the child logger will log.

    Returns:
        str: The child logger's inherited name.
    """
    # This syntax allows the new module's logger to inherit the parent logger's properties.
    return PARENT_LOGGER_NAME + "." + module_name


# ------------------------------------------
# BEHAVIOUR DRIVEN TESTING CUSTOM LOG LEVELS
# ------------------------------------------

# The logging module initialises such definitions with the log level numbers and then converts them to strings. This code initialises the
# definitions with strings immediately. You may have to use the numerical definitions for certain features in the logging module.
logging.FEATURE = FEATURE_LOG_NAME
logging.SCENARIO = SCENARIO_LOG_NAME
logging.STEP = STEP_LOG_NAME
logging.RESULT = RESULT_LOG_NAME
logging.REPORT = REPORT_LOG_NAME

logging.addLevelName(FEATURE_LOG_LEVEL, logging.FEATURE)
logging.addLevelName(SCENARIO_LOG_LEVEL, logging.SCENARIO)
logging.addLevelName(STEP_LOG_LEVEL, logging.STEP)
logging.addLevelName(RESULT_LOG_LEVEL, logging.RESULT)
logging.addLevelName(REPORT_LOG_LEVEL, logging.REPORT)

logging.Logger.feature = feature
logging.Logger.scenario = scenario
logging.Logger.step = step
logging.Logger.result = result
logging.Logger.report = report


# -------------
# PARENT LOGGER
# -------------

parent_logger = logging.getLogger(PARENT_LOGGER_NAME)
parent_logger.setLevel(
    logging.DEBUG
)  # Set the minimum logging level for the logger. Any handlers are restricted to this minimum.

formatter = logging.Formatter(
    "| %(asctime)s | %(levelname)-8s | %(module)-25s | %(message)-77s |"
)

# Set up a handler to log all logs of level 'DEBUG' or higher to a file.
debug_file_handler = logging.FileHandler("debug.log", mode="w")
debug_file_handler.setLevel(logging.DEBUG)
debug_file_handler.setFormatter(formatter)
parent_logger.addHandler(debug_file_handler)

# Set up a handler to log to 'stdout'.
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)
parent_logger.addHandler(stdout_handler)

# Set up a handler to log the Behaviour Driven Test logs to a file.
test_file_handler = logging.FileHandler("test.log", mode="w")
test_file_handler.setLevel(
    logging.NOTSET
)  # Select the lowest logging level so this handler can see all the logs.
test_file_handler.setFormatter(formatter)
levels_to_capture = [
    FEATURE_LOG_LEVEL,
    SCENARIO_LOG_LEVEL,
    STEP_LOG_LEVEL,
    RESULT_LOG_LEVEL,
    REPORT_LOG_LEVEL,
]
test_file_handler.addFilter(LogLevelFilter(levels_to_capture))
parent_logger.addHandler(test_file_handler)
