"""Pytest fixtures for async tests."""

# pylint: disable=wrong-import-position,redefined-outer-name,unused-import
import asyncio
import sys
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# ensure project root is on sys.path so top-level packages (like `core`) import correctly
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.models import Base


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create a temporary in-memory sqlite async engine for tests."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)

    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture()
async def async_session(
    async_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a test and rollback at the end."""
    async_session_factory = async_sessionmaker(
        bind=async_engine, expire_on_commit=False
    )

    async with async_session_factory() as session:
        yield session
        await session.rollback()
