import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_and_get_book(client: AsyncClient):
    book_data = {
        "title": "Тестовая Книга",
        "author": "Тестовый Автор",
        "publisher": "Тестовое Издательство",
        "published_date": "2026-07-10",
        "page_count": 350,
        "language": "Russian"
    }

    response = await client.post("/api/v1/books/", json=book_data)
    
    # Если упадет, мы сразу увидим текст ошибки Pydantic прямо в консоли pytest
    assert response.status_code == 201, f"Error is: {response.json()}"
    
    data = response.json()
    assert data["title"] == book_data["title"]
    assert "uid" in data
    
    book_uid = data["uid"]

    get_response = await client.get(f"/api/v1/books/{book_uid}")
    assert get_response.status_code == 200, f"Error book response: {get_response.json()}"
    
    get_data = get_response.json()
    assert get_data["title"] == book_data["title"]


@pytest.mark.asyncio
async def test_get_non_existent_book(client: AsyncClient):
    fake_uid = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.get(f"/api/v1/books/{fake_uid}")
    
    # Выводим детали 422 ошибки
    assert response.status_code == 404, f"Checking for 404 error {response.json()}"