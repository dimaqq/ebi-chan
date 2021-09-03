import os

import pytest


@pytest.fixture
def server():
    return os.environ.get("EBI_HOST", "localhost")
