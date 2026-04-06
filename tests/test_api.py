import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, get_db
from app import models

client = TestClient(app)

# Создаём тестовые таблицы
models.Base.metadata.create_all(bind=engine)

# Глобальная переменная для хранения ID созданного перевала
test_pereval_id = None


def test_create_pereval():
    """Тест создания перевала"""
    global test_pereval_id

    response = client.post("/submitData/", json={
        "beauty_title": "Тестовый перевал",
        "title": "Тестовая гора",
        "other_titles": "Тест",
        "connect": "Тестовая связь",
        "user": {
            "email": "test@example.com",
            "phone": "+79991234567",
            "full_name": "Тестов Тест Тестович"
        },
        "coords": {
            "latitude": 55.7558,
            "longitude": 37.6176,
            "height": 500
        },
        "level": {
            "winter": "2A",
            "summer": "1B",
            "autumn": "2A",
            "spring": "1B"
        },
        "images": [
            {"data": "https://example.com/test.jpg", "title": "Тестовое фото"}
        ]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["message"] == "Успех. Перевал добавлен"
    assert "id" in data

    test_pereval_id = data["id"]


def test_get_pereval():
    """Тест получения перевала по ID"""
    assert test_pereval_id is not None, "Сначала выполните test_create_pereval"

    response = client.get(f"/submitData/{test_pereval_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_pereval_id
    assert data["title"] == "Тестовая гора"
    assert data["status"] == "new"


def test_update_pereval():
    """Тест редактирования перевала"""
    assert test_pereval_id is not None, "Сначала выполните test_create_pereval"

    response = client.patch(f"/submitData/{test_pereval_id}", json={
        "title": "Обновлённое название",
        "coords": {
            "latitude": 56.0000,
            "longitude": 38.0000,
            "height": 600
        }
    })

    assert response.status_code == 200
    data = response.json()
    assert data["state"] == 1
    assert data["message"] == "Успешно обновлено"

    # Проверяем, что обновилось
    get_response = client.get(f"/submitData/{test_pereval_id}")
    assert get_response.json()["title"] == "Обновлённое название"


def test_update_status():
    """Тест обновления статуса модерации"""
    assert test_pereval_id is not None, "Сначала выполните test_create_pereval"

    response = client.patch(f"/submitData/{test_pereval_id}/status?status=accepted")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "Статус обновлён"

    get_response = client.get(f"/submitData/{test_pereval_id}")
    assert get_response.json()["status"] == "accepted"