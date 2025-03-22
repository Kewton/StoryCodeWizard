import pytest
from app.chat import communicate


def test_communicate():
    result = communicate("TestProject", "test-model", "Python", "")
    assert isinstance(result, list), "Result should be a list"
    assert len(result) > 0, "Result should not be empty"
