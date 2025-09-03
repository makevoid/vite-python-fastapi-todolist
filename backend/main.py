import os
import tempfile
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List
from peewee import SqliteDatabase

from models import db, Todo
from schemas import TodoResponse, TodoCreate, TodoUpdate
from controllers import TodoController

# Configure database based on environment
def get_database():
    app_env = os.getenv("APP_ENV", "development")
    if app_env == "test":
        # Use temporary database for tests
        test_db_file = os.path.join(tempfile.gettempdir(), "test_todo.db")
        test_db = SqliteDatabase(test_db_file)
        Todo._meta.database = test_db
        return test_db
    else:
        # Use default database
        return db

# Lifespan context manager for database
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    current_db = get_database()
    if current_db.is_closed():
        current_db.connect()
    current_db.create_tables([Todo], safe=True)

    yield

    # Shutdown
    if not current_db.is_closed():
        current_db.close()

# Create FastAPI app with environment-specific title
def create_app():
    app_env = os.getenv("APP_ENV", "development")
    title = "Todo API - Test" if app_env == "test" else "Todo API"
    return FastAPI(title=title, lifespan=lifespan)

app = create_app()

# Add CORS middleware with environment-specific origins
def get_cors_origins():
    app_env = os.getenv("APP_ENV", "development")
    if app_env == "test":
        return ["http://localhost:5174"]  # Different port for test frontend
    else:
        return ["http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize controller
todo_controller = TodoController()

# Routes
@app.get("/")
def read_root():
    return {"message": "Todo API", "version": "1.0.0"}

@app.get("/api/todos", response_model=List[TodoResponse])
def get_all_todos():
    """Get all todos"""
    return todo_controller.get_all_todos()

@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    return todo_controller.get_todo(todo_id)

@app.post("/api/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate):
    """Create a new todo"""
    return todo_controller.create_todo(todo)

@app.put("/api/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, update: TodoUpdate):
    """Update a todo's details"""
    return todo_controller.update_todo(todo_id, update)

@app.post("/api/todos/{todo_id}/toggle", response_model=TodoResponse)
def toggle_todo_completion(todo_id: int):
    """Toggle a todo's completion status"""
    return todo_controller.toggle_todo_completion(todo_id)

@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int):
    """Delete a todo"""
    return todo_controller.delete_todo(todo_id)

if __name__ == "__main__":
    import uvicorn
    app_env = os.getenv("APP_ENV", "development")
    port = 8001 if app_env == "test" else 8000
    reload = app_env != "test"  # Don't use reload in test mode
    uvicorn.run(app, host="0.0.0.0", port=port, reload=reload)
