"""A testing configuration for the 'pytest' framework.

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

import os
import pytest
pytest.register_assert_rewrite('fpabart')
import fpabart

from bart_logging import create_logger, Result, archive_report
from pytest import FixtureRequest, Item
from typing import Callable
from appium import webdriver



logger = create_logger(__name__)

# Define the fixtures file. This must be defined in 'conftest.py' because 'pytest' does not intend for the user to
# import fixtures directly from fixture files to test files.
pytest_plugins = ["bart_fixtures"]


@pytest.fixture(scope="module", autouse=True)
def log_feature_name(request: FixtureRequest):
    """Log the feature's name.

    The feature's name is the test file's name (i.e., the module's name).

    Args:
        request (FixtureRequest): The fixture request.
    """
    # The file's name is the feature's name.
    test_file_name = request.module.__file__
    test_file_name = os.path.basename(test_file_name)  # Remove the path from the file's name.
    test_file_name = os.path.splitext(test_file_name)[0]  # Extract the file's name and extension, and keep the name.
    logger.feature(test_file_name)


@pytest.fixture(scope="function", autouse=True)
def log_scenario(request: FixtureRequest):
    """Log the scenario's name.

    Args:
        request (FixtureRequest): The fixture request.
    """
    test_function = request.function

    if hasattr(test_function, "scenario"):
        scenario_decorator_text = test_function.scenario
        logger.scenario(scenario_decorator_text)
    else:
        pytest.fail(f"The function {test_function.__name__} does not have a scenario decorator!")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Item):
    """Store the result for each test function.

    Args:
        item (Item): The test invocation item.
    """
    outcome = yield
    rep = outcome.get_result()

    # Store the result in the test invocation item.
    setattr(item, "rep_" + rep.when, rep)


def scenario(name: str):
    """Add a 'scenario' attribute to a function via a decorator.

    Args:
        name (str): The scenario's name.
    """

    def decorator(function: Callable):
        """Add a 'scenario' attribute to a function via a decorator.

        Args:
            function (Callable): The function to be decorated.
        """
        function.scenario = name

        return function

    return decorator


def step(step_text: str) -> None:
    """Log a test step.

    Args:
        step_text (str): The step's text.
    """
    logger.step(step_text)


def report(report_text: str) -> None:
    """Log a piece of information to the report.

    Args:
        report_text (str): The text to report.
    """
    logger.report(report_text)


def pytest_runtest_teardown(item: Item):
    """Log the test result for each test function.

    Args:
        item (Item): The test invocation item.
    """
    if hasattr(item, "rep_call"):
        if item.rep_call.passed:
            logger.result(Result.PASS)
        elif item.rep_call.failed:
            logger.result(Result.FAIL)


def pytest_sessionfinish():
    """After all the tests finish, create the report and archive all files from the test run."""
    archive_report()
