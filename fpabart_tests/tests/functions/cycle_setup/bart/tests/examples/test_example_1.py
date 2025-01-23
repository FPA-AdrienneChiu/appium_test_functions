"""Example Test Suite 1

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

import bart


@bart.scenario(
    "Add some numbers together correctly to simulate a passing test with one passing step and no failing steps"
)
def test_pass_1():
    """1 pass, 0 failures."""
    bart.report("Here is some information at the top of the report.")
    bart.report("You can add multiple lines.")
    bart.step("Add 3 and 3")
    assert (3 + 3) == (6)


@bart.scenario("Add some numbers together correctly to simulate a passing test with multiple passing steps")
def test_pass_2():
    """2 passes, 0 failures."""
    bart.step("Add 2 and 2")
    assert (2 + 2) == (4)
    bart.step("Add 1 and 1")
    assert (1 + 1) == (2)


@bart.scenario("Import a fixture and verify its contents")
def test_pass_3(example):
    """1 pass, 0 failures.

    Args:
        my_fixture (str): The example fixture.
    """
    bart.step("Verify a test can import a fixture")
    assert example == "An example fixture!"


@bart.scenario(
    "Add some numbers together incorrectly to simulate a failing test with one failing step and no passing steps"
)
def test_fail_1():
    """0 passes, 1 failure."""
    bart.step("5 plus 5 is 55")
    assert (5 + 5) == (55)


@bart.scenario(
    "Add some numbers together incorrectly to simulate a failing test with one passing step and one failing step"
)
def test_fail_2():
    """1 pass, 1 failure."""
    bart.step("Add 1 and 1")
    assert (1 + 1) == (2)
    bart.step("5 plus 5 is 55")
    assert (5 + 5) == (55)


@bart.scenario(
    "Add some numbers together incorrectly to simulate a failing test with one passing step and two failing steps"
)
def test_fail_3():
    """1 pass, 2 failures."""
    bart.step("Add 1 and 1")
    assert (1 + 1) == (2)
    bart.step("5 plus 5 is 55")
    assert (5 + 5) == (55)
    bart.step("8 plus 8 is 18 (this step will not run)")
    assert (8 + 8) == (18)


@bart.scenario(
    "Add some numbers together incorrectly to simulate a failing test with two passing steps and two failing steps"
)
def test_fail_4():
    """2 passes, 2 failures."""
    bart.step("Add 1 and 1")
    assert (1 + 1) == (2)
    bart.step("Add 5 and 5")
    assert (5 + 5) == (10)
    bart.step("8 plus 8 is 18")
    assert (8 + 8) == (18)
    bart.step("5 plus 5 is 55 (this step will not run)")
    assert (5 + 5) == (55)
