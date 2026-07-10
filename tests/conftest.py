import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
# Импортируем AsyncSession именно из sqlmodel!
from sqlmodel.ext.asyncio.session import AsyncSession 
from httpx import AsyncClient, ASGITransport
import jwt
from datetime import datetime, timedelta, timezone

from src import app
from src.db.main import get_session
from src.config import Config
import src.auth.dependencies as auth_deps

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)

# Настраиваем фабрику так, чтобы она штамповала сессии SQLModel
TestingSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession,  # Используем AsyncSession из sqlmodel
    expire_on_commit=False
)

@pytest.fixture(scope="session", autouse=True)
async def init_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture(autouse=True)
def mock_blocklist(monkeypatch):
    """Глушит проверку Redis блок-листа, всегда возвращая False."""
    async def mock_token_in_blocklist(jti: str) -> bool:
        return False
    monkeypatch.setattr(auth_deps, "token_in_blocklist", mock_token_in_blocklist)

@pytest.fixture
def valid_test_token() -> str:
    """Генерирует полноценный JWT-токен со всеми техническими полями."""
    payload = {
        "user": {
            "user_uid": "test-user-uuid-1111",
            "email": "test_user@example.com",
            "role": "admin"
        },
        "role": "admin",
        "jti": "test-random-jti-uid-value",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    return jwt.encode(payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

@pytest.fixture
async def client(db_session: AsyncSession, valid_test_token: str) -> AsyncGenerator[AsyncClient, None]:
    """Создает асинхронный клиент для эндпоинтов."""
    async def override_get_session():
        yield db_session

    app.dependency_overrides.clear()
    app.dependency_overrides[get_session] = override_get_session

    headers = {"Authorization": f"Bearer {valid_test_token}"}
    
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test", 
        headers=headers
    ) as ac:
        yield ac
        
    app.dependency_overrides.clear()