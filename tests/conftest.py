import os
import secrets

import aiohttp
import pytest


@pytest.fixture
def random_name():
    return secrets.token_hex(nbytes=4)


@pytest.fixture
def another_name():
    return secrets.token_hex(nbytes=4)


@pytest.fixture
def server():
    return os.environ.get("EBI_HOST", "localhost")


@pytest.fixture
async def client():
    async with aiohttp.ClientSession() as client:
        yield client
