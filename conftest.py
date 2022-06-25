import pytest
from pytest_html import extras
from py.xml import html

# Report Customization and Enhancing Hooks
# https://pytest-html.readthedocs.io/en/latest/user_guide.html


def pytest_html_report_title(report):
    # Report Title
    report.title = "CircleMakerTestResult"


def pytest_html_results_summary(prefix, summary, postfix):
    # Additional summary information
    prefix.extend(
        [
            html.p(
                "This is the result of running the circlemaker's tests"
            )
        ]
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Formatting the Duration Column
    outcome = yield
    report = outcome.get_result()
    setattr(report, "duration_formatter", "%H:%M:%S.%f")