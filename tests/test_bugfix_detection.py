# tests/test_bugfix_detection.py
import pytest
import pandas as pd
from src.extract_bugfix_commits import is_bugfix

@pytest.mark.parametrize("message", [
    "Fix crash when loading configuration",
    "Resolves issue #45",
    "BUG: memory leak in loop",
    "patch applied for security vulnerability",
    "error handling improved", 
])
def test_detect_valid_bug_fixes(message):
    assert is_bugfix(message) is True

@pytest.mark.parametrize("message", [
    "Update README documentation",
    "Refactoring code structure",
    "Merge branch 'main' into feature-branch",
    "Bump version to 1.0.1",
    "Adding new feature: User Authentication",
])
def test_ignore_non_bug_fixes(message):
    assert is_bugfix(message) is False

@pytest.mark.parametrize("message", [
    "Fix typo in README documentation", 
    "Merge pull request #12: fix typo", 
    "Update docs to fix broken link", 
])
def test_ignore_false_positives(message):
    assert is_bugfix(message) is False

@pytest.mark.parametrize("message", [
    None,
    pd.NA,
    "", 
    12345, 
])
def test_handle_invalid_inputs(message):
    assert is_bugfix(message) is False