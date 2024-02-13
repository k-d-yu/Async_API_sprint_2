from asyncio import AbstractEventLoop, get_event_loop_policy
import pytest

from utils.helpers import HTTPResponse

from settings import API_URL
from typing import Iterator


@pytest.fixture(scope='session')
def event_loop() -> Iterator[AbstractEventLoop]:
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope='session')
def make_get_request(session_fastapi):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = API_URL + method
        async with session_fastapi.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
