# ✨ Todo List App

A simple, modern CRUD todo list application built with FastAPI and vanilla JavaScript.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange)

## Features

- ✅ Create, read, update, and delete todos
- 💾 SQLite database for persistent storage
- 🎨 Modern dark theme with smooth animations
- 🐳 Dockerized for easy deployment
- 🚀 CI/CD with GitHub Actions

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite (aiosqlite) |
| Container | Docker |
| CI/CD | GitHub Actions |

## Quick Start

### Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\Activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload
```

Open **http://localhost:8000**

### Docker

```bash
docker-compose up --build
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/todos` | List all todos |
| `POST` | `/api/todos` | Create a new todo |
| `PUT` | `/api/todos/{id}` | Update a todo |
| `DELETE` | `/api/todos/{id}` | Delete a todo |

## Testing

```bash
pytest -v
```

## CI/CD

- **CI**: Runs tests on every push and PR to `master`
- **CD**: Builds Docker image, pushes to GHCR, and deploys to VPS
