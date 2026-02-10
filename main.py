"""
Todo List CRUD API
A simple FastAPI application for managing todo items with SQLite persistence.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import aiosqlite
import uuid
import os

DATABASE_PATH = os.getenv("DATABASE_PATH", "todos.db")


# Pydantic models
class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class Todo(BaseModel):
    id: str
    title: str
    completed: bool


# Database initialization
async def init_db():
    """Initialize the SQLite database and create tables if they don't exist."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
        """)
        await db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    await init_db()
    yield


# Initialize FastAPI app
app = FastAPI(title="Todo List API", version="1.0.0", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Endpoints
@app.get("/api/todos", response_model=list[Todo])
async def get_todos():
    """Get all todos from the database."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT id, title, completed FROM todos ORDER BY rowid DESC") as cursor:
            rows = await cursor.fetchall()
            return [
                Todo(id=row["id"], title=row["title"], completed=bool(row["completed"]))
                for row in rows
            ]


@app.post("/api/todos", response_model=Todo)
async def create_todo(todo_data: TodoCreate):
    """Create a new todo in the database."""
    todo_id = str(uuid.uuid4())
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO todos (id, title, completed) VALUES (?, ?, ?)",
            (todo_id, todo_data.title, 0)
        )
        await db.commit()
    return Todo(id=todo_id, title=todo_data.title, completed=False)


@app.put("/api/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo_data: TodoUpdate):
    """Update an existing todo in the database."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        
        # Check if todo exists
        async with db.execute("SELECT id, title, completed FROM todos WHERE id = ?", (todo_id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Todo not found")
            
            current_title = row["title"]
            current_completed = bool(row["completed"])
        
        # Update fields
        new_title = todo_data.title if todo_data.title is not None else current_title
        new_completed = todo_data.completed if todo_data.completed is not None else current_completed
        
        await db.execute(
            "UPDATE todos SET title = ?, completed = ? WHERE id = ?",
            (new_title, int(new_completed), todo_id)
        )
        await db.commit()
    
    return Todo(id=todo_id, title=new_title, completed=new_completed)


@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: str):
    """Delete a todo from the database."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Check if todo exists
        async with db.execute("SELECT id FROM todos WHERE id = ?", (todo_id,)) as cursor:
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="Todo not found")
        
        await db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        await db.commit()
    
    return {"message": "Todo deleted successfully"}


# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    """Serve the main HTML page."""
    return FileResponse("static/index.html")
