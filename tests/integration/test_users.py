import pytest
from uuid import uuid4

from app.models.user import User

@pytest.mark.asyncio
async def test_create_user_returns_serialized_id(client):
    email = f"integration_user_1_{uuid4().hex[:8]}@mail.com"
    payload = {
        "email": email,
        "password": "MyStrongPass123!",
        "first_name": "Mahmud",
        "last_name": "Jewel",
    }

    response = await client.post("/users/", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "New user created"
    assert isinstance(body["data"]["id"], str)
    assert len(body["data"]["id"]) > 0
    assert body["data"]["email"] == payload["email"]
    assert "password" not in body["data"]

    inserted_user = await User.find_one(User.email == payload["email"])
    assert inserted_user is not None
    assert inserted_user.first_name == payload["first_name"]
    assert inserted_user.last_name == payload["last_name"]


@pytest.mark.asyncio
async def test_create_user_with_duplicate_email_returns_400(client):
    email = f"integration_user_2_{uuid4().hex[:8]}@mail.com"
    payload = {
        "email": email,
        "password": "MyStrongPass123!",
        "first_name": "Mahmud",
        "last_name": "Jewel",
    }

    first_response = await client.post("/users/", json=payload)
    second_response = await client.post("/users/", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json() == {"detail": "User already exists"}
    assert await User.find(User.email == payload["email"]).count() == 1
