from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List

from database import db
from models import Todo
from schemas import TodoResponse, TodoCreate, TodoUpdate
from controllers import TodoController
from config.environment import APP_TITLE, CORS_ORIGINS, SERVER_HOST, SERVER_PORT, RELOAD

# Get database from models
def get_database():
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
    return FastAPI(title=APP_TITLE, lifespan=lifespan)

app = create_app()

# Add CORS middleware with environment-specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
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
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, reload=RELOAD)
