"""Define the hooks.

This file is required by the 'fpabart' module if we wish to take advantage of the module's hooks. We can track step
timings, set up the test environment, and create reports using these hooks. See fpabart's documentation for more
information.

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

import fpabart as bart
import logging
import shutil
import sys

from datetime import datetime
from pathlib import Path


START_TIMESTAMP_KEY = "start_timestamp"
END_TIMESTAMP_KEY = "end_timestamp"

FPABART_JSON_FILE_RELATIVE_PATH = Path("fpabart.json")
REPORTS_DIRECTORY_RELATIVE_PATH = Path("reports")
LATEST_REPORT_DIRECTORY_RELATIVE_PATH = REPORTS_DIRECTORY_RELATIVE_PATH / Path("latest")


logger = logging.getLogger()


def _get_timestamp() -> str:
    """Get the current timestamp.

    Returns:
        str: The timestamp in the format: "YYYY-MM-DD HH:MM:SS,mmm". For example: "2024-11-15 11:49:27.375".
    """
    now = datetime.now()  # noqa: DTZ005
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

    return timestamp


def _create_report() -> None:
    """Create and archive the test report.

    The report and log files will appear in the 'reports/latest' directory and the 'reports/YYYY-mm-dd_HH-MM-SS'
    directory.
    """
    import modules.fpabart_reporting.reporter as reporter

    # Create the 'reports' directory (if it does not already exist).
    directory = REPORTS_DIRECTORY_RELATIVE_PATH
    directory.mkdir(parents=True, exist_ok=True)

    directory = LATEST_REPORT_DIRECTORY_RELATIVE_PATH

    # Clean the 'latest' reports directory by deleting it.
    if directory.exists():
        shutil.rmtree(directory)

    # Create/recreate the 'latest' reports directory.
    directory.mkdir(parents=True, exist_ok=True)

    # Move the 'fpabart.json' file into the 'latest' reports directory.
    file = FPABART_JSON_FILE_RELATIVE_PATH
    file.rename(LATEST_REPORT_DIRECTORY_RELATIVE_PATH / file)

    reporter.create_report(
        Path.cwd() / LATEST_REPORT_DIRECTORY_RELATIVE_PATH
    )  # Create the report with the 'fpabart.json' file.

    # Move the log file to the 'latest' reports directory.
    file = Path("all.log")
    file.rename(LATEST_REPORT_DIRECTORY_RELATIVE_PATH / file)

    # Duplicate the 'latest' report directory but name it after the current timestamp. A directory of this name should
    # not already exist.
    timestamp = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))  # noqa: DTZ005
    shutil.copytree(LATEST_REPORT_DIRECTORY_RELATIVE_PATH, REPORTS_DIRECTORY_RELATIVE_PATH / Path(timestamp))


def process_command_line_arguments(command_line_arguments: list):
    """Process the command line arguments.

    This gets called before 'pytest' sees the command line arguments.

    Args:
        command_line_arguments (list): The command line arguments.
    """
    logger.info(f"Command line arguments: {command_line_arguments}")


def on_session_opening():
    """'fpabart' runs this once at the start of the test session."""
    bart.session_attribute(START_TIMESTAMP_KEY, _get_timestamp())

    sys.path.append(str(Path.cwd().parent))
    logger.debug(f"Updated the Python path to include the root of the repository! The Python path is now: {sys.path}")


def before_feature():
    """'fpabart' runs this at the start of each feature."""
    bart.feature_attribute(START_TIMESTAMP_KEY, _get_timestamp())


def before_scenario():
    """'fpabart' runs this at the start of each scenario."""
    bart.scenario_attribute(START_TIMESTAMP_KEY, _get_timestamp())


def before_step():
    """'fpabart' runs this at the start of each step."""
    bart.step_attribute(START_TIMESTAMP_KEY, _get_timestamp())


def after_step():
    """'fpabart' runs this after each step."""
    bart.step_attribute(END_TIMESTAMP_KEY, _get_timestamp())


def after_scenario():
    """'fpabart' runs this after each scenario."""
    bart.scenario_attribute(END_TIMESTAMP_KEY, _get_timestamp())


def after_feature():
    """'fpabart' runs this after each feature."""
    bart.feature_attribute(END_TIMESTAMP_KEY, _get_timestamp())


def on_session_closing():
    """'fpabart' runs this once at the end of the test session."""
    bart.session_attribute(END_TIMESTAMP_KEY, _get_timestamp())


def last_hook():
    """'fpabart' runs this once after it generates the 'fpabart.json' file."""
    _create_report()
