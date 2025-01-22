"""Example Test Suite 2

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


@bart.scenario("Print a string but do not log any steps")
def test_print():
    # The tester may forget to log any steps, or the test may crash before it logs its first step. In such a case,
    # the reporting system must create the report. It must not crash because it cannot find any steps.
    bart.report("You can add information to the top of the report at any point.")
    print("Hello, World!")
