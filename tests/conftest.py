import uuid
import pytest
from sqlalchemy import text
from typing import AsyncGenerator
from sqlmodel import text, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession 
from httpx import AsyncClient, ASGITransport
import jwt
from datetime import datetime, timedelta, timezone

from src import app
from src.db.main import get_session
from src.config import Config
from src.db.models import User  
import src.auth.dependencies as auth_deps

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)

TestingSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
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
    
    async def mock_token_in_blocklist(jti: str) -> bool:
        return False
    monkeypatch.setattr(auth_deps, "token_in_blocklist", mock_token_in_blocklist)

@pytest.fixture
def valid_test_token() -> str:
    
    expiry_timestamp = int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp())
    test_user_uuid = "12345678123456781234567812345678"
    payload = {
        "user": {
            "user_uid": str(test_user_uuid), 
            "email": "test_user@example.com",
            "role": "admin"
        },
        "role": "admin",
        "jti": "test-random-jti-uid-value",
        "exp": expiry_timestamp
    }
    return jwt.encode(payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

from sqlmodel import SQLModel  

@pytest.fixture
async def client(db_session: AsyncSession, valid_test_token: str) -> AsyncGenerator[AsyncClient, None]:
    
    connection = await db_session.connection()
    await connection.run_sync(SQLModel.metadata.drop_all)
    await connection.run_sync(SQLModel.metadata.create_all)
    await db_session.commit()
    

   
    test_user_uuid = uuid.UUID('12345678123456781234567812345678')
    test_user = User(
        uid=test_user_uuid,
        email="test_user@example.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        role="admin",
        password_hash="fake_hash_value",
        is_verified=True
    )
    
    
    db_session.add(test_user)
    await db_session.commit()
    
    from sqlalchemy import text

    result = await db_session.execute(
        text("SELECT uid, typeof(uid), email FROM users")
    )

    print(result.fetchall())

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