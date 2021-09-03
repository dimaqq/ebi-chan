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
    name = request.match_info["name"]
    STATE.get().names.setdefault(name, Record.new())
    record = STATE.get().names[name]
    record.backoff *= 2
    record.timestamp = time.monotonic()
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
        return self.timestamp + self.backoff

    @classmethod
    def new(cls):
        return cls(0.05, time.monotonic())


@dataclass
class State:
    names: Dict[str, Record]


if __name__ == "__main__":
    web.run_app(app, port=7890, reuse_address=True)
