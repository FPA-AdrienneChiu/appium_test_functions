"""Create an HTML report from the "fpabart.json" file.

This file has one public function which creates the report. All other functions are helper functions and are intended
to be private. The public function saves a directory to a global variable and the helper functions create all the
report files within that directory.

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

import json
import PyPDF2

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from weasyprint import HTML


INDEX_HTML_FILE_NAME = "index.html"
REPORT_PDF_FILE_NAME = "report.pdf"
STYLES_CSS_FILE_NAME = "styles.css"

_directory = Path.cwd()  # The CWD is a default path. The public method will update this variable.


def _get_fpabart_json_data() -> dict:
    """Get the JSON data from "fpabart.json".

    Returns:
        dict: The JSON data from "fpabart.json".
    """
    with open(_directory / "fpabart.json", "r") as file:
        json_data = json.load(file)

    return json_data


def _get_script_parent_directory() -> Path:
    """Get the absolute path to this file's parent directory (this function, not the calling function).

    Returns:
        Path: The absolute path to this file's parent directory (this function, not the calling function).
    """
    return Path(__file__).resolve().parent


def _get_overall_result(json_data: dict) -> str:
    """Get the overall result.

    Args:
        json_data (dict): The JSON data from "fpabart.json".

    Returns:
        str: "pass" or "fail".
    """
    result_string = ""

    if json_data.get("result"):
        result_string = "pass"
    else:
        result_string = "fail"

    return result_string


def _get_summary_data(json_data: dict) -> dict:
    """Extract the pass/fail metrics for the features, scenarios, and steps.

    Args:
        json_data (dict): The JSON data from "fpabart.json".

    Returns:
        dict: A dictionary which defines "features_passed", "features_failed", "features_total", "feature_pass_rate",
            "scenarios_passed", "scenarios_failed", "scenarios_total", "scenario_pass_rate", "steps_passed",
            "steps_failed", "steps_total", "step_pass_rate". The totals are integers and the pass rates are strings
            which include the '%' symbol.
    """
    features_passed, features_failed, features_total = 0, 0, 0
    scenarios_passed, scenarios_failed, scenarios_total = 0, 0, 0
    steps_passed, steps_failed, steps_total = 0, 0, 0

    for feature in json_data.get("features"):
        features_total += 1

        if feature.get("result"):
            features_passed += 1
        else:
            features_failed += 1

        for scenario in feature.get("scenarios"):
            scenarios_total += 1

            if scenario.get("result"):
                scenarios_passed += 1
            else:
                scenarios_failed += 1

            for step in scenario.get("steps"):
                steps_total += 1

                if step.get("result"):
                    steps_passed += 1
                else:
                    steps_failed += 1

    zero_percent_string = "0%"

    if features_total == 0:
        feature_pass_rate = zero_percent_string
    else:
        feature_pass_rate = features_passed / features_total
        feature_pass_rate = str(round(feature_pass_rate * 100, 1)) + "%"

    if scenarios_total == 0:
        scenario_pass_rate = zero_percent_string
    else:
        scenario_pass_rate = scenarios_passed / scenarios_total
        scenario_pass_rate = str(round(scenario_pass_rate * 100, 1)) + "%"

    if steps_passed == 0:
        step_pass_rate = zero_percent_string
    else:
        step_pass_rate = steps_passed / steps_total
        step_pass_rate = str(round(step_pass_rate * 100, 1)) + "%"

    return {
        "features_passed": features_passed,
        "features_failed": features_failed,
        "features_total": features_total,
        "feature_pass_rate": feature_pass_rate,
        "scenarios_passed": scenarios_passed,
        "scenarios_failed": scenarios_failed,
        "scenarios_total": scenarios_total,
        "scenario_pass_rate": scenario_pass_rate,
        "steps_passed": steps_passed,
        "steps_failed": steps_failed,
        "steps_total": steps_total,
        "step_pass_rate": step_pass_rate,
    }


def _get_session_attributes(json_data: dict) -> list:
    """Get the session attributes from the "fpabart.json" file.

    This function only extracts attributes whose values are strings.

    Args:
        json_data (dict): The JSON data from "fpabart.json".

    Returns:
        list: A list of dictionaries, one for each attribute. Each dictionary has two keys, one called "key" and one
            called "value". The former key's value is the attribute's key and the latter key's value is the attribute's
            value.
    """
    attributes_from_json = json_data.get("attributes")
    attributes = []

    for attribute_key in attributes_from_json:
        attribute_value = attributes_from_json.get(attribute_key)

        if type(attribute_value) is str:
            attributes.append({"key": attribute_key, "value": attribute_value})

    return attributes


def _get_toc_entries(json_data: dict) -> list:
    """Get the entries for the table of contents.

    Args:
        json_data (dict): The JSON data from "fpabart.json".

    Returns:
        list: A list of dictionaries, one for each feature and scenario. Each dictionary defines: "is_feature"
            (Boolean), "number" (integer), "name" (string), "result_class" (string), and "result_text" (string).
    """
    features = json_data.get("features")

    toc_entries = []
    feature_number = 1

    for feature in features:
        feature_toc_entry = {"is_feature": True, "number": feature_number, "name": feature.get("name")}

        if feature.get("result"):
            feature_toc_entry.update({"result_class": "pass", "result_text": "PASS"})
        else:
            feature_toc_entry.update({"result_class": "fail", "result_text": "FAIL"})

        toc_entries.append(feature_toc_entry)

        scenario_number = 1

        for scenario in feature.get("scenarios"):
            scenario_toc_entry = {"is_feature": False, "number": scenario_number, "name": scenario.get("name")}

            if scenario.get("result"):
                scenario_toc_entry.update({"result_class": "pass", "result_text": "PASS"})
            else:
                scenario_toc_entry.update({"result_class": "fail", "result_text": "FAIL"})

            toc_entries.append(scenario_toc_entry)

            scenario_number += 1

        feature_number += 1

    return toc_entries


def _get_features(json_data: dict) -> list:
    """Get the feature data.

    Args:
        json_data (dict): The JSON data from "fpabart.json".

    Returns:
        list: A list of dictionaries, one for each feature. The features contain one or more scenarios and the
            scenarios contain zero or more steps. A feature dictionary has a name (string), a result class (string),
            result text (string), a list of scenarios, and a feature number (an integer, for HTML links). A scenario
            dictionary has a name (string), a result class (string), result text (string), a list of steps, and a
            scenario number (an integer, for HTML links). A step has a name (string), and a result class (string).
    """
    features = json_data.get("features")

    feature_dicts = []
    feature_number = 1

    for feature in features:
        feature_dict = {"number": feature_number, "name": feature.get("name")}

        if feature.get("result"):
            feature_dict.update({"result_class": "pass"})
            feature_dict.update({"result_text": "PASS"})
        else:
            feature_dict.update({"result_class": "fail"})
            feature_dict.update({"result_text": "FAIL"})

        scenario_dicts = []
        scenario_number = 1

        for scenario in feature.get("scenarios"):
            scenario_dict = {"number": scenario_number, "name": scenario.get("name")}

            if scenario.get("result"):
                scenario_dict.update({"result_class": "pass"})
                scenario_dict.update({"result_text": "PASS"})
            else:
                scenario_dict.update({"result_class": "fail"})
                scenario_dict.update({"result_text": "FAIL"})

            step_dicts = []

            for step in scenario.get("steps"):
                step_dict = {"name": step.get("name")}

                if step.get("result"):
                    step_dict.update({"result_class": "pass"})
                else:
                    step_dict.update({"result_class": "fail"})

                step_dicts.append(step_dict)

            scenario_dict.update({"steps": step_dicts})
            scenario_dicts.append(scenario_dict)
            scenario_number += 1

        feature_dict.update({"scenarios": scenario_dicts})
        feature_dicts.append(feature_dict)
        feature_number += 1

    return feature_dicts


def _get_current_year() -> int:
    """Get the current year.

    Returns:
        int: The current year.
    """
    return datetime.now().year  # noqa: DTZ005


def _create_html_report(
    overall_result: str,
    session_attributes: list,
    summary_data: dict,
    toc_entries: list,
    features: list,
    year_report_generated: int,
) -> None:
    """Create the HTML report using the template.

    Args:
        overall_result (str): "pass" or "fail".
        session_attributes (list): A list of dictionaries, one for each attribute. Each dictionary has two keys, one
            called "key" and one called "value". The former key's value is the attribute's key and the latter key's
            value is the attribute's value.
        summary_data (dict): A dictionary which defines "features_passed", "features_failed", "features_total", "feature_pass_rate",
            "scenarios_passed", "scenarios_failed", "scenarios_total", "scenario_pass_rate", "steps_passed",
            "steps_failed", "steps_total", "step_pass_rate". The totals are integers and the pass rates are strings
            which include the '%' symbol.
        toc_entries (list): A list of dictionaries, one for each feature and scenario. Each dictionary defines: "is_feature"
            (Boolean), "number" (integer), "name" (string), "result_class" (string), and "result_text" (string).
        features (list): A list of dictionaries, one for each feature. The features contain one or more scenarios and the
            scenarios contain zero or more steps. A feature dictionary has a name (string), a result class (string),
            result text (string), a list of scenarios, and a feature number (an integer, for HTML links). A scenario
            dictionary has a name (string), a result class (string), result text (string), a list of steps, and a
            scenario number (an integer, for HTML links). A step has a name (string), and a result class (string).
        year_report_generated (int): The current year (for the copyright statement).
    """
    environment = Environment(autoescape=True, loader=FileSystemLoader(_get_script_parent_directory()))
    template = environment.get_template("template.html")

    html_report = template.render(
        overall_result_class=overall_result,
        overall_result_text=overall_result.upper(),
        session_attributes=session_attributes,
        summary_data=summary_data,
        toc_entries=toc_entries,
        features=features,
        year_report_generated=year_report_generated,
    )

    with open(_directory / INDEX_HTML_FILE_NAME, "w") as file:
        file.write(html_report)


def _create_css_file(page_height: int) -> None:
    """Create the CSS file.

    Args:
        page_height (int): The page's height in mm.
    """
    environment = Environment(autoescape=True, loader=FileSystemLoader(_get_script_parent_directory()))
    template = environment.get_template("template.css")

    css_styles = {"page_height": page_height}
    output = template.render(css_styles)

    with open(_directory / STYLES_CSS_FILE_NAME, "w") as file:
        file.write(output)


def _create_pdf_file() -> None:
    """Create the single-page PDF file.

    This function creates a PDF report where each page is 297mm high (the height of an A3 page). Then it counts the
    number of pages in this PDF file and creates a new PDF file with a page height of 297mm multiplied by the number
    of pages in the original PDF. This creates a single-page PDF.
    """
    a3_page_height = 297

    _create_css_file(a3_page_height)  # Configure the CSS file to use the default page height.

    with open(_directory / INDEX_HTML_FILE_NAME, "r") as file:
        html_content = file.read()

    # Create the PDF file with the default page heights.
    HTML(string=html_content).write_pdf(
        _directory / REPORT_PDF_FILE_NAME, stylesheets=[_directory / STYLES_CSS_FILE_NAME]
    )

    # Count the number of pages in the PDF file.
    with open(_directory / REPORT_PDF_FILE_NAME, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

    # Configure the CSS file such that, should it get turned into a PDF, all of its content will go onto one page.
    _create_css_file(a3_page_height * num_pages)

    # Create the single-page PDF.
    HTML(string=html_content).write_pdf(
        _directory / REPORT_PDF_FILE_NAME, stylesheets=[_directory / STYLES_CSS_FILE_NAME]
    )


def create_report(directory: Path) -> None:
    """Create a report from the 'fpabart.json' file.

    The report consists of an HTML + CSS file pair, and a PDF file.

    Args:
        directory (Path): The directory containing the 'fpabart.json' file. The report files will appear here too.
    """
    global _directory
    _directory = directory

    json_data = _get_fpabart_json_data()

    overall_result = _get_overall_result(json_data)
    session_attributes = _get_session_attributes(json_data)
    summary_data = _get_summary_data(json_data)
    toc_entries = _get_toc_entries(json_data)
    features = _get_features(json_data)
    year_report_generated = _get_current_year()

    _create_html_report(overall_result, session_attributes, summary_data, toc_entries, features, year_report_generated)
    _create_pdf_file()
