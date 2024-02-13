import aiohttp
import pytest


@pytest.fixture(scope='session')
async def session_fastapi():
    session_fastapi = aiohttp.ClientSession()
    yield session_fastapi
    await session_fastapi.close()
