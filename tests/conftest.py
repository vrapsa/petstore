import pytest

from helpers.api.client import Api


@pytest.fixture
def api() -> Api:
    return Api()
