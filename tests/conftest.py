import os
import sys
from pathlib import Path
from uuid import uuid4

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient


TEST_MONGODB_URL = os.getenv("TEST_MONGODB_URL", "mongodb://localhost:27017")
TEST_DB_BASE_NAME = os.getenv("TEST_DB_NAME", "fastapi_mongodb_boilerplate_test")
TEST_DB_ISOLATED = os.getenv("TEST_DB_ISOLATED", "0") == "1"
TEST_DB_RUN_SUFFIX = os.getenv("TEST_DB_RUN_SUFFIX", uuid4().hex[:8])
TEST_DB_NAME = (
    f"{TEST_DB_BASE_NAME}_{TEST_DB_RUN_SUFFIX}" if TEST_DB_ISOLATED else TEST_DB_BASE_NAME
)

# App reads from app.utils.env module-level variables. Set before importing app.
os.environ["MONGODB_URL"] = TEST_MONGODB_URL
os.environ["ClUSTER_NAME"] = TEST_DB_NAME
os.environ.setdefault("SECRET_KEY", "integration-test-secret-key")
os.environ.setdefault("REFRESH_SECRET_KEY", "integration-test-refresh-secret-key")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_DAYS", "7")
os.environ.setdefault("REFRESH_TOKEN_EXPIRE_DAYS", "30")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.main import create_app


@pytest_asyncio.fixture(scope="session")
async def ensure_test_db_available():
    client = AsyncIOMotorClient(TEST_MONGODB_URL, serverSelectionTimeoutMS=2000)
    try:
        await client.admin.command("ping")
    except Exception as exc:
        pytest.skip(f"MongoDB test instance not reachable: {exc}")
    finally:
        client.close()

    yield


@pytest_asyncio.fixture()
async def client(ensure_test_db_available):
    app = create_app()
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
        ) as async_client:
            yield async_client
