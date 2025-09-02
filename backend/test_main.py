"""
Test version of main.py that uses a separate test database and runs on different ports
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from peewee import SqliteDatabase
import os
import tempfile

# Create test database in temp directory
test_db_file = os.path.join(tempfile.gettempdir(), "test_todo.db")
test_db = SqliteDatabase(test_db_file)

# Import and configure models for test database
from models import Todo
Todo._meta.database = test_db

# Import other modules
from controllers import TodoController
from schemas import TodoCreate, TodoResponse, TodoUpdate

app = FastAPI(title="Todo API - Test", version="1.0.0")

# Configure CORS for test
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # Different port for test frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize test database
def init_test_db():
    if test_db.is_closed():
        test_db.connect()
    test_db.create_tables([Todo], safe=True)

# Initialize controller
controller = TodoController()

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Todo API - Test", "version": "1.0.0"}

# Todo endpoints
@app.get("/api/todos", response_model=list[TodoResponse])
async def get_todos():
    return controller.get_all_todos()

@app.post("/api/todos", response_model=TodoResponse)
async def create_todo(todo: TodoCreate):
    return controller.create_todo(todo)

@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int):
    return controller.get_todo(todo_id)

@app.put("/api/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    return controller.update_todo(todo_id, todo_update)

@app.post("/api/todos/{todo_id}/toggle", response_model=TodoResponse)
async def toggle_todo_completion(todo_id: int):
    return controller.toggle_todo_completion(todo_id)

@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: int):
    return controller.delete_todo(todo_id)

# Startup event
@app.on_event("startup")
async def startup_event():
    init_test_db()

if __name__ == "__main__":
    init_test_db()
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Different port for test backend