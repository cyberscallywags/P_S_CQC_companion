"""_summary_ ."""

import logging
import os
import sys

import pytest

from src.logging_config import setup_json_logging

logger = logging.getLogger(__name__)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


@pytest.fixture(scope="session", autouse=True)
def setup_teardown_session():
    """_summary_ ."""
    logger.info("\n*** Setup before session ***\n")
    yield
    logger.info("\n*** Setup before session ***\n")


@pytest.fixture(scope="function", autouse=True)
def setup_teardown_function():
    """_summary_ ."""
    logger.info("\n*** Setup before tests ***\n")
    yield
    logger.info("\n*** Teardown after tests ***\n")


@pytest.fixture
def important_value():
    """_summary_ ."""
    importantValue = "Very important value"

    logger.info(f"*** importantValue ***:  {importantValue}")
    return importantValue


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """_summary_ ."""
    pre_commit = os.getenv("PRE_COMMIT", "0") == "1"
    if pre_commit:
        # Console-only, file redirected to /tmp to avoid repo changes
        setup_json_logging(
            app_name="tests",
            to_console=True,
            log_file="/tmp/testonsave-tests.log",
        )
    else:
        setup_json_logging(app_name="tests", to_console=False)
