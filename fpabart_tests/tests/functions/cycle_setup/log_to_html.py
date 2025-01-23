"""."""

import os

from result import Result


REPORT_FILE_NAME = "index.html"


class HtmlReporter:
    """Convert '.log' files into '.html' reports."""

    def _start_report(self, feature: str) -> None:
        """Start a test report.

        Args:
            feature (str): The name of the feature under test.
        """
        if os.path.exists(REPORT_FILE_NAME):
            os.remove(REPORT_FILE_NAME)

        with open(REPORT_FILE_NAME, "a") as report:
            report.write("""<!DOCTYPE html>\n""")
            report.write("""<html lang="en">\n""")
            report.write("""<head>\n""")
            report.write("""    <meta charset="UTF-8">\n""")
            report.write(
                """    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n"""
            )
            report.write("""    <link rel="stylesheet" href="styles.css">\n""")
            report.write("""    <title>Report</title>\n""")
            report.write("""</head>\n""")
            report.write("""<body>\n""")

            report.write("""    <h1 class="centred-text">""")
            report.write(feature)
            report.write("""</h1>\n""")

        self._add_info()

    def _add_info(self) -> None:
        """Add the stored report information entries to the information section of the report."""
        with open(REPORT_FILE_NAME, "a") as report:
            report.write("""    <div id="info">\n""")

            for report_info_string in self.report_info_strings:
                report.write("""        <p class="centred-text">""")
                report.write(report_info_string)
                report.write("""</p>\n""")

            report.write("""    </div>\n""")

    def _start_scenario(self, name: str) -> None:
        """Start a scenario.

        Args:
            scenario (str): The scenario's name.
        """
        with open(REPORT_FILE_NAME, "a") as report:
            self._end_scenario()  # If a previous scenario had been started, end it.

            report.write("""    <h3 class="centred-text scenario-heading">""")
            report.write(name)
            report.write("""</h3>\n""")
            report.write("""    <table class="steps-table">\n""")
            report.write("""        <tr>\n""")
            report.write(
                """            <th class="steps-table-timestamp-column steps-table-heading">Timestamp</th>\n"""
            )
            report.write(
                """            <th class="steps-table-step-column steps-table-heading">Step</th>\n"""
            )
            report.write(
                """            <th class="steps-table-result-column steps-table-heading">Result</th>\n"""
            )
            report.write("""        </tr>\n""")

        self.scenario_started = True

    def _start_step(self, timestamp: str, step: str) -> None:
        """Start a step.

        Args:
            timestamp (str): The step's timestamp.
            step (str): The step.
        """
        self.current_timestamp = timestamp
        self.current_step = step

    def _end_step(self, result: Result) -> None:
        """End the current step.

        Args:
            result (Result): The step's result.
        """
        with open(REPORT_FILE_NAME, "a") as report:
            report.write("""        <tr>\n""")
            report.write("""            <td class="steps-table-data">""")
            report.write(self.current_timestamp)
            report.write("""</td>\n""")

            report.write("""            <td class="steps-table-data">""")
            report.write(self.current_step)
            report.write("""</td>\n""")

            if result == Result.PASS:
                report.write(
                    """            <td class="steps-table-data steps-table-result-pass">"""
                )
            else:
                report.write(
                    """            <td class="steps-table-data steps-table-result-fail">"""
                )

            report.write(result.value)
            report.write("""</td>\n""")

            report.write("""        </tr>\n""")

    def _end_report(self) -> None:
        """End the report."""
        with open(REPORT_FILE_NAME, "a") as report:
            self._end_scenario()

            report.write("""</body>\n""")
            report.write("""</html>\n""")

    def _end_scenario(self) -> None:
        """If a scenario has been started, end it."""
        if self.scenario_started:
            with open(REPORT_FILE_NAME, "a") as report:
                report.write("    </table>\n")

    def _extract_log_components(self, log_line: str) -> list:
        """Extract the components from a log line.

        Args:
            log_line (str): The log line.

        Returns:
            list: The components as strings.
        """
        log_components = log_line.split("|")  # Split the log into its components.

        # Clean up each entry in the log's component list.
        for log_component_index in range(0, len(log_components)):
            log_component = log_components[log_component_index]
            log_component = (
                log_component.strip()
            )  # Get rid of any preceding and trailing whitespace.
            log_components[log_component_index] = log_component

        return log_components

    def create_report(self) -> None:
        """Convert a '.log' file into a '.html' report."""
        self.scenario_started = False
        self.report_info_strings = []  # Reset the report information list.

        with open("test.log", "r") as log_file:
            log_file_lines = log_file.readlines()

            # Gather all the report information entries from the log file.
            for log_line in log_file_lines:
                log_components = self._extract_log_components(log_line)
                log_level = log_components[2]

                if log_level == "REPORT":
                    message = log_components[1]
                    message = message[0 : message.index(",")]
                    self.report_info_strings.append(message)

            # Handle each log in the log file.
            for log_line in log_file_lines:
                log_components = self._extract_log_components(log_line)

                timestamp = log_components[1]
                log_level = log_components[2]
                message = log_components[4]

                if log_level == "FEATURE":
                    self._start_report(message)
                elif log_level == "SCENARIO":
                    self._start_scenario(message)
                elif log_level == "STEP":
                    self._start_step(timestamp, message)
                elif log_level == "RESULT":
                    if "PASS" in message:
                        self._end_step(Result.PASS)
                    else:
                        self._end_step(Result.FAIL)

        self._end_report()


reporter = HtmlReporter()
reporter.create_report()
