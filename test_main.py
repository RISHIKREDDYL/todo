"""
Tests for the Todo List CRUD API.
"""

import os
import pytest
from fastapi.testclient import TestClient

# Use a separate test database
os.environ["DATABASE_PATH"] = "test_todos.db"

from main import app


@pytest.fixture(autouse=True)
def clean_db():
    """Remove test database before and after each test."""
    if os.path.exists("test_todos.db"):
        os.remove("test_todos.db")
    yield
    if os.path.exists("test_todos.db"):
        os.remove("test_todos.db")


@pytest.fixture()
def client():
    """Create a test client with lifespan events."""
    with TestClient(app) as c:
        yield c


def test_get_todos_empty(client):
    """GET /api/todos returns empty list initially."""
    response = client.get("/api/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_todo(client):
    """POST /api/todos creates a new todo."""
    response = client.post("/api/todos", json={"title": "Test todo"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test todo"
    assert data["completed"] is False
    assert "id" in data


def test_get_todos_after_create(client):
    """GET /api/todos returns created todos."""
    client.post("/api/todos", json={"title": "First"})
    client.post("/api/todos", json={"title": "Second"})

    response = client.get("/api/todos")
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 2


def test_update_todo(client):
    """PUT /api/todos/{id} updates a todo."""
    create_res = client.post("/api/todos", json={"title": "Original"})
    todo_id = create_res.json()["id"]

    response = client.put(f"/api/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True
    assert response.json()["title"] == "Original"


def test_update_todo_title(client):
    """PUT /api/todos/{id} updates the title."""
    create_res = client.post("/api/todos", json={"title": "Old title"})
    todo_id = create_res.json()["id"]

    response = client.put(f"/api/todos/{todo_id}", json={"title": "New title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_update_nonexistent_todo(client):
    """PUT /api/todos/{id} returns 404 for missing todo."""
    response = client.put("/api/todos/fake-id", json={"completed": True})
    assert response.status_code == 404


def test_delete_todo(client):
    """DELETE /api/todos/{id} removes a todo."""
    create_res = client.post("/api/todos", json={"title": "To delete"})
    todo_id = create_res.json()["id"]

    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 200

    # Verify it's gone
    get_res = client.get("/api/todos")
    assert len(get_res.json()) == 0


def test_delete_nonexistent_todo(client):
    """DELETE /api/todos/{id} returns 404 for missing todo."""
    response = client.delete("/api/todos/fake-id")
    assert response.status_code == 404


def test_root_serves_html(client):
    """GET / serves the index.html page."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
