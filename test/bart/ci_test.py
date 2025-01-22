"""Run the example tests and verify the outputted log, HTML, and CSS files.

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

We use pytest to log the features, scenarios, steps, results, and general report messages. We also use it to generate a
report at the end. This test script verifies pytest logs the correct things in the correct order, and that it generates
the report correctly.

Usage:
    python3 test/bart/ci_test.py

    The exit code is 0 if the test passes. The exit code is not 0 if the test fails.

    Most of the output from this script gets logged to 'ci_test_output'.
"""

import os
import re

from datetime import datetime


def verify_log():
    """Verify the log is correct."""
    with open("reports/latest/test.log", "r") as report_log_file:
        report_log_lines = report_log_file.readlines()

    with open("test/bart/benchmark_files/benchmark_test.log", "r") as benchmark_log_file:
        benchmark_log_lines = benchmark_log_file.readlines()

    # Verify the files contain the same number of lines before iterating over each line.
    num_lines = len(report_log_lines)
    assert num_lines == len(benchmark_log_lines)

    timestamp_regex = re.compile("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}")

    line_checks = 0

    for line_index in range(0, num_lines):
        report_line = report_log_lines[line_index]
        benchmark_line = benchmark_log_lines[line_index]

        report_line_match = timestamp_regex.search(report_line)
        benchmark_line_match = timestamp_regex.search(benchmark_line)

        # Remove the timestamp from the report line because timestamps change.
        if report_line_match is not None:
            report_line_matched_text = report_line_match.group()
            report_line = report_line.replace(report_line_matched_text, "")

        # Remove the timestamp from the benchmark line because timestamps change.
        if benchmark_line_match is not None:
            benchmark_line_matched_text = benchmark_line_match.group()
            benchmark_line = benchmark_line.replace(benchmark_line_matched_text, "")

        assert report_line == benchmark_line  # They should match exactly.

        line_checks += 1

    # Verify the test checked all of the lines.
    assert line_checks == num_lines


def verify_html():
    """Verify the HTML is correct."""
    with open("reports/latest/index.html", "r") as report_html_file:
        report_html_lines = report_html_file.readlines()

    with open("test/bart/benchmark_files/benchmark_index.html", "r") as benchmark_html_file:
        benchmark_html_lines = benchmark_html_file.readlines()

    # Verify the files contain the same number of lines before iterating over each line.
    num_lines = len(report_html_lines)
    assert num_lines == len(benchmark_html_lines)

    timestamp_regex = re.compile("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}")
    copyright_regex = re.compile("&copy; \d\d\d\d Fisher & Paykel Appliances Limited\. All rights reserved\.")

    line_checks = 0

    for line_index in range(0, num_lines):
        report_line = report_html_lines[line_index]
        benchmark_line = benchmark_html_lines[line_index]

        report_line_timestamp_match = timestamp_regex.search(report_line)
        benchmark_line_timestamp_match = timestamp_regex.search(benchmark_line)

        # Remove the timestamp from the report line because timestamps change.
        if report_line_timestamp_match is not None:
            report_line_matched_timestamp_text = report_line_timestamp_match.group()
            report_line = report_line.replace(report_line_matched_timestamp_text, "")

        # Remove the timestamp from the benchmark line because timestamps change.
        if benchmark_line_timestamp_match is not None:
            benchmark_line_matched_timestamp_text = benchmark_line_timestamp_match.group()
            benchmark_line = benchmark_line.replace(benchmark_line_matched_timestamp_text, "")

        benchmark_line_copyright_match = copyright_regex.search(benchmark_line)

        # Replace the copyright year with the current year. This should match the year in the report.
        if benchmark_line_copyright_match is not None:
            benchmark_line_copyright_matched_text = benchmark_line_copyright_match.group()
            new_copyright_text = (
                "&copy; " + str(datetime.now().year) + " Fisher & Paykel Appliances Limited. All rights reserved."
            )
            benchmark_line = benchmark_line.replace(benchmark_line_copyright_matched_text, new_copyright_text)

        assert report_line == benchmark_line  # They should match exactly.

        line_checks += 1

    # Verify the test checked all of the lines.
    assert line_checks == num_lines


def verify_stylesheet():
    """Verify the stylesheet is correct."""
    with open("reports/latest/styles.css", "r") as report_stylesheet_file:
        report_stylesheet_contents = report_stylesheet_file.read()

    with open("test/bart/benchmark_files/benchmark_styles.css", "r") as benchmark_stylesheet_file:
        benchmark_stylesheet_contents = benchmark_stylesheet_file.read()

    # The stylesheet in the report should match the benchmark exactly.
    assert report_stylesheet_contents == benchmark_stylesheet_contents


if __name__ == "__main__":
    # Run the example tests.
    os.system(
        "python3 -m pytest bart/tests/examples/test_example_1.py bart/tests/examples/test_example_2.py 1> ci_test_output"
    )

    # Verify the output files are correct.
    verify_log()
    verify_html()
    verify_stylesheet()

    print("Test passed!")
