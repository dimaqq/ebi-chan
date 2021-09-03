import secrets
import time
from contextlib import contextmanager

import aiohttp
import pytest

pytestmark = [pytest.mark.asyncio]


@contextmanager
def timed(save_to=[]):
    start = time.time()
    try:
        yield
    finally:
        save_to.append(time.time() - start)


def canonical_time(time):
    for exp in range(10):
        threshold = 0.1 * 2 ** exp
        if threshold <= time < threshold * 2:
            return threshold


async def test_sequential_requests(server):
    tag = secrets.token_hex(4)
    log = []
    async with aiohttp.ClientSession() as client:
        for _ in range(4):
            with timed(save_to=log):
                resp = await client.get(f"http://{ server }:7890/backoff/{ tag }")
                assert resp.status in (200, 204)
    assert [canonical_time(t) for t in log] == [0.1, 0.2, 0.4, 0.8]
