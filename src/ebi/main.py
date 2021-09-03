import asyncio
import time
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any, Dict

from aiohttp import web

app = web.Application()
routes = web.RouteTableDef()
STATE: ContextVar["State"] = ContextVar("STATE")


@routes.get("/debug")
async def debug(request):
    return web.json_response({"foo": 42})


@routes.get("/backoff/{name:.+}")
async def backoff(request):
    now = time.monotonic()
    name = request.match_info["name"]

    STATE.get().names.setdefault(name, Record.new(now))

    record = STATE.get().names[name]
    if now >= record.expiration:
        record.backoff = 0.1
    else:
        record.backoff *= 2
    record.timestamp = now

    await asyncio.sleep(record.backoff)
    raise web.HTTPNoContent()


async def startup(app):
    STATE.set(State(names={}))


app.add_routes(routes)
app.on_startup.append(startup)


@dataclass
class Record:
    backoff: float
    timestamp: float

    @property
    def expiration(self):
        return self.timestamp + self.backoff * 2

    @classmethod
    def new(cls, timestamp):
        return cls(0, timestamp)


@dataclass
class State:
    names: Dict[str, Record]


if __name__ == "__main__":
    web.run_app(app, port=7890, reuse_address=True)
