"""An extension of Python's default logging package for BART.

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
import os
import shutil
import sys

from datetime import datetime
from enum import Enum
from logging import Logger, LogRecord
from pathlib import Path
from weasyprint import HTML


PARENT_LOGGER_NAME = "parent_logger"

# BART's custom log levels.
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

DEBUG_LOG_FILE_NAME = "debug.log"
TEST_LOG_FILE_NAME = "test.log"

REPORTS_DIRECTORY = Path("reports")
REPORTS_LATEST_DIRECTORY = REPORTS_DIRECTORY / Path("latest")


class Result(Enum):
    """Define the possible results for an action."""

    PASS = "PASS"
    FAIL = "FAIL"


class LogLevelFilter(logging.Filter):
    """Filter the logs to only record logs of certain levels."""

    def __init__(self, levels: list):
        """Construct a LogLevelFilter.

        Args:
            levels (list): The log levels for the filter to capture. The filter will ignore logs of all other levels.
        """
        self.levels = levels

    def filter(self, record: LogRecord) -> bool:
        """Determine if the specified record should be logged or filtered out.

        Args:
            record (LogRecord): The record to check.

        Returns:
            bool: True if the record should be logged or False if the record should not be logged.
        """
        return record.levelno in self.levels


class LogConverter:
    """Convert ".log" files into ".html" and ".pdf" reports."""

    PASS_TEXT = "PASS"
    FAIL_TEXT = "FAIL"

    def _start_report(self) -> None:
        """Start a test report."""
        if os.path.exists(self.html_file_path):
            os.remove(self.html_file_path)

        with open(self.html_file_path, "a") as report:
            with open("bart/index.html", "r") as index_html_file:
                index_html = index_html_file.read()

            # Start the HTML file.
            index_html = index_html.replace("YYYY", str(datetime.now().year))  # Add current year.
            report.write(index_html)

            # Start the body with the copyright statement then the title.
            report.write("""<body>\n""")
            report.write("""    <header id="top-copyright">""")
            report.write(
                """&copy; """ + str(datetime.now().year) + " Fisher & Paykel Appliances Limited. All rights reserved."
            )
            report.write("""</header>\n""")
            report.write("""    <h1 id="report-title">Report</h1>\n""")  # Hard-code the main title.

    def _add_info(self) -> None:
        """Extract the report information logs and add them to the top of the report."""
        report_logs = []

        with open(self.log_file_path, "r") as log_file:
            log_file_lines = log_file.readlines()

        # Gather all the report information entries from the log file.
        for log_line in log_file_lines:
            log_components = self._extract_log_components(log_line)
            log_level = log_components[2]

            if log_level == "REPORT":
                message = log_components[4]
                report_logs.append(message)

        # Add all the report information entries to the HTML file.
        with open(self.html_file_path, "a") as report:
            report.write("""    <div id="info">\n""")

            for report_log in report_logs:
                report.write("""        <p class="centred-text">""")
                report.write(report_log)
                report.write("""</p>\n""")

            report.write("""    </div>\n""")

    def _add_feature(self, feature_name: str) -> None:
        """Add a feature heading to the report.

        Args:
            feature_name (str): The feature's name.
        """
        # Add the feature title.
        with open(self.html_file_path, "a") as report:
            report.write("""    <h2 class="feature-title">""")
            report.write(feature_name)
            report.write("""</h2>\n""")

    def _start_scenario(self, name: str) -> None:
        """Start a scenario.

        Args:
            name (str): The scenario's name.
        """
        # Start the scenario's table with the first row. This contains the headings.
        with open(self.html_file_path, "a") as report:
            report.write("""    <p class="scenario-title">""")
            report.write(name)
            report.write("""</p>\n""")
            report.write("""    <table class="steps-table">\n""")
            report.write("""        <tr>\n""")
            report.write(
                """            <th class="steps-table-timestamp-column steps-table-heading">Timestamp</th>\n"""
            )
            report.write("""            <th class="steps-table-step-column steps-table-heading">Step</th>\n""")
            report.write("""            <th class="steps-table-result-column steps-table-heading">Result</th>\n""")
            report.write("""        </tr>\n""")

        self._current_step_in_progress = False  # Reset this variable since we have not encountered a step yet.

    def _start_step(self, timestamp: str, step: str) -> None:
        """Start a step and end the previous step if necessary.

        Args:
            timestamp (str): The step's timestamp.
            step (str): The step.
        """
        # If a previous step was in progress, and now there is a new step, the previous step must have passed.
        if self._current_step_in_progress:
            self._end_step(self.PASS_TEXT)

        # Store the step's details until required.
        self._current_step_timestamp = timestamp
        self._current_step = step
        self._current_step_in_progress = True

    def _end_step(self, result: str) -> None:
        """End the current step.

        Args:
            result (str): The step's result.
        """
        # If a is step in progress, put its pre-recorded timestamp and name, plus the step's result, in the table.
        if self._current_step_in_progress:
            self._report_step(self._current_step_timestamp, self._current_step, result)

    def _end_scenario(self, result: str, timestamp: str) -> None:
        """Report the last step's result and end the scenario's step table.

        Args:
            result (str): The scenario's result.
            timestamp (str): The time at which the scenario finished.
        """
        self._end_step(result)  # The last step's result will match the scenario's result.

        # Add an "END" step in case there are no steps in the test. This ensures the table is not empty and consists
        # of more than just the heading row. The end step also marks the final timestamp which can be useful. For
        # example, the reader may want to calculate how long the final step took to run. The end step's result will
        # match the scenario's result.
        self._report_step(timestamp, "RESULT", result)

        # End the scenario's table.
        with open(self.html_file_path, "a") as report:
            report.write("    </table>\n")

    def _end_report(self) -> None:
        """End the report."""
        # End the HTML document.
        with open(self.html_file_path, "a") as report:
            report.write("""</body>\n""")
            report.write("""</html>\n""")

    def _extract_log_components(self, log_line: str) -> list:
        """Extract the components from a log line.

        Args:
            log_line (str): The log line.

        Returns:
            list: The components as strings.
        """
        log_components = log_line.split("|")  # Split the log into its components which are separated by a '|'.

        # Clean each entry in the log's component list.
        for log_component_index in range(0, len(log_components)):
            log_component = log_components[log_component_index]
            log_component = log_component.strip()  # Get rid of any preceding and trailing whitespace.
            log_components[log_component_index] = log_component

        return log_components

    def _report_step(self, timestamp: str, step: str, result: str) -> None:
        """Add a row to the step table.

        Args:
            timestamp (str): The step's timestamp.
            step (str): The step.
            result (str): The step's result.
        """
        with open(self.html_file_path, "a") as report:
            # Add the timestamp's cell.
            report.write("""        <tr>\n""")
            report.write("""            <td class="steps-table-data">""")
            report.write(timestamp)
            report.write("""</td>\n""")

            # Add the step's cell.
            report.write("""            <td class="steps-table-data">""")
            report.write(step)
            report.write("""</td>\n""")

            # Determine how to decorate the result text.
            if result == self.PASS_TEXT:
                report.write("""            <td class="steps-table-data steps-table-result-pass">""")
            else:
                report.write("""            <td class="steps-table-data steps-table-result-fail">""")

            # Add the result.
            report.write(result)
            report.write("""</td>\n""")

            report.write("""        </tr>\n""")  # End the step's row.

    def convert_to_report(self, log_file_path: str, html_file_path: str, pdf_file_path: str) -> None:
        """Convert a log file to an HTML report and a PDF report.

        Args:
            log_file_path (str): The path to the log file. This is the input.
            html_file_path (str): The path to the HTML file. This is an output file.
            pdf_file_path (str): The path to the PDF file. This is an output file.
        """
        self.log_file_path = log_file_path
        self.html_file_path = html_file_path

        # Certain helper methods must be called in a certain order. These are the first two.
        self._start_report()
        self._add_info()

        with open(self.log_file_path, "r") as log_file:
            log_file_lines = log_file.readlines()

            # Handle each log in the log file.
            for log_line in log_file_lines:
                log_components = self._extract_log_components(log_line)

                timestamp = log_components[1]
                log_level = log_components[2]
                message = log_components[4]

                # Handle the log message.
                if log_level == "FEATURE":
                    self._add_feature(message)
                elif log_level == "SCENARIO":
                    self._start_scenario(message)
                elif log_level == "STEP":
                    self._start_step(timestamp, message)
                elif log_level == "RESULT":
                    self._end_scenario(message, timestamp)

        self._end_report()

        # The stylesheet lives in the same directory as this script.
        stylesheet_path_source = Path(os.path.abspath(__file__)).parent / Path("styles.css")

        # The stylesheet must sit in the same directory as the new HTML report.
        stylesheet_path_destination = Path(html_file_path).parent / Path("styles.css")
        shutil.copy(stylesheet_path_source, stylesheet_path_destination)

        html = HTML(html_file_path)
        html.write_pdf(pdf_file_path)


def feature(self: Logger, message: str, *args: tuple, **kwargs: dict) -> None:
    """Log a message with severity 'FEATURE'.

    Args:
        self (Logger): The Logger calling this function.
        message (str): The message to log.
    """
    if self.isEnabledFor(FEATURE_LOG_LEVEL):
        self._log(FEATURE_LOG_LEVEL, message, args, **kwargs)


def scenario(self: Logger, message: str, *args: tuple, **kwargs: dict) -> None:
    """Log a message with severity 'SCENARIO'.

    Args:
        self (Logger): The Logger calling this function.
        message (str): The message to log.
    """
    if self.isEnabledFor(SCENARIO_LOG_LEVEL):
        self._log(SCENARIO_LOG_LEVEL, message, args, **kwargs)


def step(self: Logger, message: str, *args: tuple, **kwargs: dict) -> None:
    """Log a message with severity 'STEP'.

    Args:
        self (Logger): The Logger calling this function.
        message (str): The message to log.
    """
    if self.isEnabledFor(STEP_LOG_LEVEL):
        self._log(STEP_LOG_LEVEL, message, args, **kwargs)


def result(self: Logger, result: Result, *args: tuple, **kwargs: dict) -> None:
    """Log a message with severity 'RESULT'.

    Args:
        self (Logger): The Logger calling this function.
        result (Result): The result to log.
    """
    if self.isEnabledFor(RESULT_LOG_LEVEL):
        self._log(RESULT_LOG_LEVEL, result.value, args, **kwargs)  # 'result.value' gets the enumerated value's string.


def report(self: Logger, message: str, *args: tuple, **kwargs: dict) -> None:
    """Log a message with severity 'REPORT'.

    Args:
        self (Logger): The Logger calling this function.
        message (str): The message to log.
    """
    if self.isEnabledFor(REPORT_LOG_LEVEL):
        self._log(REPORT_LOG_LEVEL, message, args, **kwargs)


def get_logger_name(module_name: str) -> str:
    """Determine the name for a child logger so it will inherit the parent logger's properties.

    For example, let the module's name be 'my_class'. This function will return 'PARENT_LOGGER_NAME.my_class'. This
    means the child logger will log as 'my_class', but the logging functionality will make the child logger inherit the
    parent logger's functionality.

    Args:
        module_name (str): The name of the module for which the child logger will log.

    Returns:
        str: The child logger's inherited name.
    """
    # This syntax allows the new module's logger to inherit the parent logger's properties.
    return PARENT_LOGGER_NAME + "." + module_name


def create_logger(module_name: str) -> Logger:
    """Create a custom logger for a module.

    Args:
        module_name (str): The name of the module from which the logger will log.

    Returns:
        Logger: The module's new logger.
    """
    return logging.getLogger(get_logger_name(module_name))


def archive_report():
    """Convert the log file to HTML and PDF reports, and archive all log and report files to a timestamped directory.

    The timestamped directory will be named YYYY-mm-DD_HH-MM-SS where Y = year, m = month, D = day, H = hour, M =
    minute, and S = second.
    """
    log_converter = LogConverter()
    log_converter.convert_to_report(
        REPORTS_LATEST_DIRECTORY / Path(TEST_LOG_FILE_NAME),
        REPORTS_LATEST_DIRECTORY / Path("index.html"),
        REPORTS_LATEST_DIRECTORY / Path("report.pdf"),
    )

    # Put the latest report in its own, timestamped directory. The timestamp represents when the test run finished.
    time_object = datetime.now()
    timestamp = time_object.strftime("%Y-%m-%d_%H-%M-%S")
    shutil.copytree(REPORTS_LATEST_DIRECTORY, REPORTS_DIRECTORY / Path(timestamp))


# ------------------------
# BART'S CUSTOM LOG LEVELS
# ------------------------

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


# -----------------------
# CREATE REPORT DIRECTORY
# -----------------------

# Ensure there is a reports directory.
if os.path.exists(REPORTS_DIRECTORY) is not True:
    os.mkdir(REPORTS_DIRECTORY)

# If the latest report directory already exists, delete it to purge its contents.
if os.path.exists(REPORTS_LATEST_DIRECTORY):
    shutil.rmtree(REPORTS_LATEST_DIRECTORY)

os.mkdir(REPORTS_LATEST_DIRECTORY)  # Create/recreate the latest report directory.


# -------------
# PARENT LOGGER
# -------------

parent_logger = logging.getLogger(PARENT_LOGGER_NAME)
parent_logger.setLevel(
    logging.DEBUG
)  # Set the minimum logging level for the logger. Any handlers are restricted to this minimum.

formatter = logging.Formatter("| %(asctime)s | %(levelname)-8s | %(module)-25s | %(message)-77s |")

# Set up a handler to log all logs of level 'DEBUG' or higher to a file.
debug_file_handler = logging.FileHandler(REPORTS_LATEST_DIRECTORY / DEBUG_LOG_FILE_NAME, mode="w")
debug_file_handler.setLevel(logging.DEBUG)
debug_file_handler.setFormatter(formatter)
parent_logger.addHandler(debug_file_handler)

# Set up a handler to log to 'stdout'.
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)
parent_logger.addHandler(stdout_handler)

# Set up a handler to log the Behaviour Driven Test logs to a file.
test_file_handler = logging.FileHandler(REPORTS_LATEST_DIRECTORY / TEST_LOG_FILE_NAME, mode="w")
test_file_handler.setLevel(logging.NOTSET)  # Select the lowest logging level so this handler can see all the logs.
test_file_handler.setFormatter(formatter)
levels_to_capture = [FEATURE_LOG_LEVEL, SCENARIO_LOG_LEVEL, STEP_LOG_LEVEL, RESULT_LOG_LEVEL, REPORT_LOG_LEVEL]
test_file_handler.addFilter(LogLevelFilter(levels_to_capture))
parent_logger.addHandler(test_file_handler)
