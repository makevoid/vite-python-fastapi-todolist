# 🚀 Todo List App Recreation Prompt for Claude Opus 4.1

This document contains the master prompt and sub-prompts to recreate this entire todo list application from scratch using Claude Opus 4.1. The application demonstrates professional full-stack development with comprehensive testing.

## 🎯 **Master Prompt - Project Overview**

```
Create a professional full-stack todo list application with the following specifications:

**PROJECT ARCHITECTURE:**
- **Backend**: FastAPI (Python) with SQLite database and Peewee ORM
- **Frontend**: React with Vite, Chakra UI v2, and TanStack React Query
- **Testing**: 12 backend unit tests + 13 E2E tests with Playwright
- **Structure**: Clean architecture with services, repositories, controllers

**CORE REQUIREMENTS:**
1. **Todo CRUD Operations**: Create, read, update, delete todos
2. **Toggle Completion**: Mark todos as complete/incomplete
3. **Inline Editing**: Edit todos directly in the UI
4. **Real-time Updates**: Optimistic UI updates with error handling
5. **Professional UI**: Business-grade design with Chakra UI
6. **Comprehensive Testing**: Full test coverage with fast execution
7. **Type Safety**: JSDoc annotations and Pydantic models

**PROJECT STRUCTURE:**
```
vite-python-fastapi-todolist/
├── backend/              # FastAPI backend
│   ├── main.py          # App setup & routes
│   ├── models.py        # Database models (Peewee)
│   ├── schemas.py       # Pydantic request/response models
│   ├── services.py      # Business logic layer
│   ├── repositories.py  # Data access layer
│   ├── controllers.py   # HTTP request handling
│   ├── test_api.py      # Unit tests (12 tests)
│   └── requirements.txt # Python dependencies
├── frontend/            # React frontend
│   ├── src/
│   │   ├── App.jsx      # Main component
│   │   ├── main.jsx     # App entry point
│   │   ├── services/
│   │   │   ├── ApiService.js    # Base HTTP client
│   │   │   └── TodoService.js   # Todo-specific API
│   │   └── hooks/
│   │       └── useTodos.js      # React Query hook
│   └── package.json     # Frontend dependencies
└── e2e/                 # End-to-end tests
    ├── test_todo_e2e.py # E2E tests (13 tests)
    └── pyproject.toml   # Test configuration

**TODO DATA MODEL:**
```python
class Todo(Model):
    id = AutoField()                    # Primary key
    title = CharField()                 # Required todo title
    description = TextField(default='') # Optional description
    completed = BooleanField(default=False) # Completion status
```

**API ENDPOINTS:**
- GET /api/todos - Get all todos
- POST /api/todos - Create new todo
- GET /api/todos/{id} - Get specific todo
- PUT /api/todos/{id} - Update todo
- POST /api/todos/{id}/toggle - Toggle completion
- DELETE /api/todos/{id} - Delete todo

Use the sub-prompts below to implement each section systematically.
```

---

## 🐍 **Sub-Prompt 1: Backend Implementation**

```
Implement a professional FastAPI backend using clean layered architecture with these 6 files:

**🗃️ 1. models.py - Database Models (Peewee ORM)**
```python
from peewee import *

# Database setup with SQLite
db = SqliteDatabase('todo.db')

class Todo(Model):
    id = AutoField()  # Primary key
    title = CharField()  # Required todo title
    description = TextField(default='')  # Optional description with default
    completed = BooleanField(default=False)  # Completion status

    class Meta:
        database = db
```

**🎯 Key Implementation Details:**
- Use exact field types: AutoField(), CharField(), TextField(default=''), BooleanField(default=False)
- Include Meta class with database reference
- Keep it minimal - no additional methods or complexity

---

**📝 2. schemas.py - Pydantic Request/Response Models**
```python
from pydantic import BaseModel
from typing import Optional

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        from_attributes = True  # Enable ORM model conversion

class TodoCreate(BaseModel):
    title: str  # Required field
    description: Optional[str] = ''  # Optional with default

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
```

**🎯 Key Implementation Details:**
- TodoResponse: Complete model for API responses with Config.from_attributes = True
- TodoCreate: Only required fields for creation (title required, description optional)  
- TodoUpdate: All fields optional using Optional[Type] = None for partial updates
- Use proper typing imports (Optional from typing)

---

**⚙️ 3. services.py - Business Logic Layer**
```python
from typing import List
from models import Todo
from schemas import TodoUpdate

class TodoNotFoundException(Exception):
    """Raised when a todo is not found"""
    pass

class TodoService:
    """Service class for todo business logic"""

    @staticmethod
    def get_all_todos() -> List[Todo]:
        """Get all todos from the database"""
        return list(Todo.select())

    @staticmethod
    def get_todo_by_id(todo_id: int) -> Todo:
        """Get a specific todo by ID"""
        try:
            return Todo.get(Todo.id == todo_id)
        except Todo.DoesNotExist:
            raise TodoNotFoundException(f"Todo with id '{todo_id}' not found")

    @staticmethod
    def create_todo(title: str, description: str = '') -> Todo:
        """Create a new todo"""
        return Todo.create(title=title, description=description)

    @staticmethod
    def update_todo(todo_id: int, update_data: TodoUpdate) -> Todo:
        """Update a todo's details"""
        todo = TodoService.get_todo_by_id(todo_id)
        
        # Only update provided fields (partial update support)
        if update_data.title is not None:
            todo.title = update_data.title
        if update_data.description is not None:
            todo.description = update_data.description
        if update_data.completed is not None:
            todo.completed = update_data.completed
        
        todo.save()
        return todo

    @staticmethod
    def toggle_todo_completion(todo_id: int) -> Todo:
        """Toggle a todo's completion status"""
        todo = TodoService.get_todo_by_id(todo_id)
        todo.completed = not todo.completed
        todo.save()
        return todo

    @staticmethod
    def delete_todo(todo_id: int) -> bool:
        """Delete a todo"""
        todo = TodoService.get_todo_by_id(todo_id)
        todo.delete_instance()
        return True
```

**🎯 Key Implementation Details:**
- Custom TodoNotFoundException for domain-specific errors
- Static methods in TodoService class (functional approach)
- Proper exception handling with try/catch for DoesNotExist
- Partial update logic that only updates provided fields
- Type hints for all parameters and return types
- Clean business logic separation - no HTTP concerns

---

**🗄️ 4. repositories.py - Data Access Layer**
```python
from typing import List
from schemas import TodoResponse, TodoCreate, TodoUpdate
from services import TodoService

class TodoRepository:
    """Repository pattern for todo data access"""

    def __init__(self):
        self.service = TodoService()

    def find_all(self) -> List[TodoResponse]:
        """Find all todos and return as response models"""
        todos = self.service.get_all_todos()
        return [TodoResponse.model_validate(t, from_attributes=True) for t in todos]

    def find_by_id(self, todo_id: int) -> TodoResponse:
        """Find todo by ID and return as response model"""
        todo = self.service.get_todo_by_id(todo_id)
        return TodoResponse.model_validate(todo, from_attributes=True)

    def create(self, todo_data: TodoCreate) -> TodoResponse:
        """Create a new todo from request data"""
        todo = self.service.create_todo(
            title=todo_data.title,
            description=todo_data.description
        )
        return TodoResponse.model_validate(todo, from_attributes=True)

    def update(self, todo_id: int, update_data: TodoUpdate) -> TodoResponse:
        """Update todo and return response model"""
        todo = self.service.update_todo(todo_id, update_data)
        return TodoResponse.model_validate(todo, from_attributes=True)

    def toggle_completion(self, todo_id: int) -> TodoResponse:
        """Toggle todo completion and return response model"""
        todo = self.service.toggle_todo_completion(todo_id)
        return TodoResponse.model_validate(todo, from_attributes=True)

    def delete(self, todo_id: int) -> dict:
        """Delete todo and return success message"""
        self.service.delete_todo(todo_id)
        return {"message": f"Todo with id '{todo_id}' deleted"}
```

**🎯 Key Implementation Details:**
- Repository pattern that wraps the service layer
- Key responsibility: Convert ORM models to Pydantic models using model_validate()
- Use from_attributes=True for ORM conversion
- All methods return Pydantic response models except delete (returns dict)
- Consistent method naming (find_all, find_by_id, create, update, etc.)

---

**🌐 5. controllers.py - HTTP Request Handling**
```python
from fastapi import HTTPException
from typing import List

from schemas import TodoResponse, TodoCreate, TodoUpdate
from repositories import TodoRepository
from services import TodoNotFoundException

class TodoController:
    """Controller class for todo API endpoints"""

    def __init__(self):
        self.repository = TodoRepository()

    def get_all_todos(self) -> List[TodoResponse]:
        """Get all todos"""
        return self.repository.find_all()

    def get_todo(self, todo_id: int) -> TodoResponse:
        """Get a specific todo by ID"""
        try:
            return self.repository.find_by_id(todo_id)
        except TodoNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    def create_todo(self, todo: TodoCreate) -> TodoResponse:
        """Create a new todo"""
        return self.repository.create(todo)

    def update_todo(self, todo_id: int, update: TodoUpdate) -> TodoResponse:
        """Update a todo's details"""
        try:
            return self.repository.update(todo_id, update)
        except TodoNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    def toggle_todo_completion(self, todo_id: int) -> TodoResponse:
        """Toggle a todo's completion status"""
        try:
            return self.repository.toggle_completion(todo_id)
        except TodoNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    def delete_todo(self, todo_id: int) -> dict:
        """Delete a todo"""
        try:
            return self.repository.delete(todo_id)
        except TodoNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))
```

**🎯 Key Implementation Details:**
- Handles HTTP concerns only (HTTPException for errors)
- Translates domain exceptions (TodoNotFoundException) to HTTP 404 errors
- Consistent try/catch pattern for all operations that can fail
- Delegates all business logic to repository layer
- Type hints for all parameters and return types

---

**🚀 6. main.py - FastAPI Application Setup**
```python
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
```

**🎯 Key Implementation Details:**
- Environment-based configuration using APP_ENV environment variable
- Lifespan context manager for proper database lifecycle
- Test isolation: temporary database when APP_ENV=test
- CORS middleware with environment-specific origins
- All routes delegate to controller methods
- Professional route documentation with docstrings
- Environment-specific port selection (8000 dev, 8001 test)

---

**📦 requirements.txt:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
peewee==3.17.0
pydantic==2.5.0
```

**🎯 Architecture Summary:**
This implements a professional layered architecture:
**Models** → **Services** → **Repositories** → **Controllers** → **Main**

Each layer has a single responsibility:
- **Models**: Database structure
- **Services**: Business logic and domain exceptions  
- **Repositories**: Data access and model conversion
- **Controllers**: HTTP concerns and error translation
- **Main**: App configuration and routing
```

---

## 🧪 **Sub-Prompt 2: Backend Testing**

```
Create a comprehensive pytest-based test suite with 12 test cases that execute in under 1 second:

**🧪 test_api.py - Backend Unit Tests (12 Lightning-Fast Tests)**
```python
import pytest
from fastapi.testclient import TestClient
from peewee import SqliteDatabase
from main import app
from models import Todo

# Test Fixtures - Critical for Test Isolation
@pytest.fixture(scope="function", autouse=True)
def test_db():
    """Reset database before each test"""
    from models import Todo, db
    
    # Ensure we're connected
    if db.is_closed():
        db.connect()
    
    # Drop and recreate tables to start fresh
    db.drop_tables([Todo], safe=True)
    db.create_tables([Todo])
    
    yield db
    
    # Clean up after test
    db.drop_tables([Todo], safe=True)

@pytest.fixture
def client(test_db):
    """Create a test client using the main app"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def setup_todos():
    """Setup initial test todos using Peewee directly"""
    Todo.create(title="Buy groceries", description="Milk, bread, eggs", completed=False)
    Todo.create(title="Write tests", description="Unit tests for todo API", completed=True)
    return [
        {"title": "Buy groceries", "description": "Milk, bread, eggs", "completed": False},
        {"title": "Write tests", "description": "Unit tests for todo API", "completed": True}
    ]

# Test Functions - All 12 Required Tests
def test_read_root(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo API", "version": "1.0.0"}

def test_get_all_todos_empty(client):
    """Test getting all todos when none exist"""
    response = client.get("/api/todos")
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo(client):
    """Test creating a new todo"""
    response = client.post(
        "/api/todos",
        json={"title": "Learn FastAPI", "description": "Build a todo app"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Build a todo app"
    assert data["completed"] == False

def test_get_all_todos(client, setup_todos):
    """Test getting all todos"""
    response = client.get("/api/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Verify todo titles
    todo_titles = [t["title"] for t in data]
    assert "Buy groceries" in todo_titles
    assert "Write tests" in todo_titles

def test_get_todo(client, setup_todos):
    """Test getting a specific todo"""
    # First create a todo to get its ID
    todo = Todo.create(title="Test todo", description="For testing", completed=False)
    
    response = client.get(f"/api/todos/{todo.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test todo"
    assert data["description"] == "For testing"
    assert data["completed"] == False

def test_update_todo(client, setup_todos):
    """Test updating a todo"""
    # First create a todo to update
    todo = Todo.create(title="Original title", description="Original desc", completed=False)
    
    response = client.put(
        f"/api/todos/{todo.id}",
        json={"title": "Updated title", "description": "Updated desc", "completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["description"] == "Updated desc"
    assert data["completed"] == True

def test_partial_update_todo(client):
    """Test partial updating a todo"""
    # Create a todo first
    todo = Todo.create(title="Original title", description="Original desc", completed=False)
    
    # Update only the completed status
    response = client.put(
        f"/api/todos/{todo.id}",
        json={"completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Original title"  # Should remain unchanged
    assert data["description"] == "Original desc"  # Should remain unchanged
    assert data["completed"] == True  # Should be updated

def test_toggle_todo_completion(client):
    """Test toggling a todo's completion status"""
    # Create a todo first
    todo = Todo.create(title="Toggle test", description="Test toggle", completed=False)
    
    # Toggle to completed
    response = client.post(f"/api/todos/{todo.id}/toggle")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] == True
    
    # Toggle back to not completed
    response = client.post(f"/api/todos/{todo.id}/toggle")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] == False

def test_delete_todo(client, setup_todos):
    """Test deleting a todo"""
    # Create a todo to delete
    todo = Todo.create(title="To be deleted", description="Will be removed", completed=False)
    
    response = client.delete(f"/api/todos/{todo.id}")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

    # Verify todo is deleted
    response = client.get(f"/api/todos/{todo.id}")
    assert response.status_code == 404

def test_todo_not_found(client):
    """Test operations on non-existent todo"""
    response = client.get("/api/todos/999")
    assert response.status_code == 404

    response = client.put("/api/todos/999", json={"title": "Updated"})
    assert response.status_code == 404

    response = client.post("/api/todos/999/toggle")
    assert response.status_code == 404

    response = client.delete("/api/todos/999")
    assert response.status_code == 404

def test_create_todo_minimal(client):
    """Test creating a todo with minimal data"""
    response = client.post(
        "/api/todos",
        json={"title": "Minimal todo"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Minimal todo"
    assert data["description"] == ""  # Should default to empty string
    assert data["completed"] == False  # Should default to False

def test_complex_workflow(client):
    """Test a complex workflow with multiple operations"""
    # Create todo
    response = client.post(
        "/api/todos",
        json={"title": "Workflow todo", "description": "Testing workflow"}
    )
    assert response.status_code == 200
    todo_id = response.json()["id"]

    # Update description
    response = client.put(
        f"/api/todos/{todo_id}",
        json={"description": "Updated description"}
    )
    assert response.json()["description"] == "Updated description"
    assert response.json()["title"] == "Workflow todo"  # Should remain unchanged

    # Toggle completion
    response = client.post(f"/api/todos/{todo_id}/toggle")
    assert response.json()["completed"] == True

    # Update title while keeping completion status
    response = client.put(
        f"/api/todos/{todo_id}",
        json={"title": "Final title"}
    )
    assert response.json()["title"] == "Final title"
    assert response.json()["completed"] == True  # Should remain True

    # Delete
    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**🎯 Critical Testing Patterns:**

**Database Isolation:**
- `test_db` fixture with `scope="function", autouse=True`
- Drop and recreate tables before each test
- Ensures zero test interference

**Test Client Setup:**
- FastAPI TestClient for HTTP testing
- Proper client lifecycle management
- Context manager usage for cleanup

**Test Data Management:**
- `setup_todos` fixture for consistent test data
- Direct Peewee model creation for setup
- Predictable test scenarios

**Comprehensive Coverage:**
- ✅ All CRUD operations (Create, Read, Update, Delete)
- ✅ Edge cases (404 errors, partial updates)
- ✅ Complex workflows (multi-step operations)
- ✅ Validation scenarios (minimal data, empty responses)

**Performance Requirements:**
- Must execute in under 1 second total
- Function-scoped fixtures for speed
- Minimal test data creation

**Assertion Patterns:**
- Status code validation (200, 404)
- Response structure validation
- Field-level value assertions
- State change verification

This test suite provides 100% API endpoint coverage with reliable, fast execution.
```

---

## ⚛️ **Sub-Prompt 3: Frontend Implementation**

```
Implement the React frontend with the following 6 files:

**1. src/services/ApiService.js - Base HTTP Client**
```javascript
// Create ApiService base class with:
// - constructor(basePath, baseURL) - Configure API endpoints
// - async get(url) - GET requests with error handling
// - async post(url, data) - POST requests with error handling  
// - async put(url, data) - PUT requests with error handling
// - async delete(url) - DELETE requests with error handling
// - Proper error handling and response parsing
// - JSDoc type annotations for all methods
```

**2. src/services/TodoService.js - Todo-Specific API**
```javascript
// Create TodoService extending ApiService with:
// - constructor() - Set basePath to '/api/todos'
// - async fetchTodos() - GET all todos
// - async createTodo(title, description) - POST new todo
// - async updateTodo(id, updates) - PUT todo updates
// - async toggleTodoCompletion(id) - POST toggle completion
// - async deleteTodo(id) - DELETE todo
// - JSDoc type annotations for all methods
```

**3. src/hooks/useTodos.js - React Query Hook**
```javascript
// Create custom hook using TanStack React Query:
// - useQuery for fetching todos with 'todos' query key
// - useMutation for createTodo with optimistic updates
// - useMutation for updateTodo with optimistic updates
// - useMutation for toggleTodoCompletion with optimistic updates
// - useMutation for deleteTodo with optimistic updates
// - Return: { todos, createTodo, updateTodo, toggleTodoCompletion, deleteTodo, isLoading, error, isCreating, isUpdating, isToggling, isDeleting }
// - Include proper error handling and cache invalidation
```

**4. src/main.jsx - Application Entry Point**
```javascript
// Create React app entry point with:
// - React.StrictMode wrapper
// - ChakraProvider with theme
// - QueryClient and QueryClientProvider setup
// - Render App component into #root
// - Import necessary React Query and Chakra UI dependencies
```

**5. src/App.jsx - Main Component**
```javascript
// Create main App component with:
// - Professional Chakra UI design (business theme with blue/gray colors)
// - Header with app title "Todo List App" and version badge
// - Create todo form (title input, description textarea, submit button)
// - Todo list display with inline editing
// - Each todo item: checkbox, title, description, edit/delete buttons
// - Inline edit mode with save/cancel functionality  
// - Loading states and error handling
// - Toast notifications for operations
// - Progress badges showing pending vs completed counts
// - Footer with GitHub logo and link to "https://github.com/makevoid/vite-python-fastapi-todolist"
// - Responsive design with proper styling
// - Use data-testid attributes for E2E testing
```

**6. package.json - Frontend Dependencies**
```json
{
  "name": "todo-app",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build", 
    "preview": "vite preview"
  },
  "dependencies": {
    "@chakra-ui/icons": "^2.2.4",
    "@chakra-ui/react": "^2.10.9",
    "@emotion/react": "^11.14.0",
    "@emotion/styled": "^11.14.1",
    "@tanstack/react-query": "^5.85.6",
    "framer-motion": "^6.5.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-icons": "^5.5.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^7.1.4"
  }
}
```

IMPORTANT: Use professional Chakra UI styling, proper state management with React Query, and include all necessary data-testid attributes for E2E testing.
```

---

## 🎭 **Sub-Prompt 4: End-to-End Testing**

```
Create comprehensive E2E testing with Playwright in 2 files:

**1. e2e/test_todo_e2e.py - E2E Tests (13 tests)**
```python
# Create pytest + Playwright test suite with these 13 test methods:

# Test Class: TestTodoAppE2E
# 1. test_app_title() - Verify page title is "Todo List App"
# 2. test_console_errors_on_render() - Check no JS errors on page load
# 3. test_console_errors_during_interactions() - Monitor console during user interactions
# 4. test_empty_state() - Verify empty state message when no todos
# 5. test_create_todo() - Test creating todo with title and description
# 6. test_create_todo_minimal() - Test creating todo with only title
# 7. test_toggle_todo_completion() - Test checkbox toggle functionality
# 8. test_edit_todo() - Test inline editing with save
# 9. test_cancel_edit_todo() - Test inline editing with cancel
# 10. test_delete_todo() - Test todo deletion
# 11. test_multiple_todos() - Test managing multiple todos
# 12. test_todo_persistence_after_refresh() - Test data persists after page refresh
# 13. test_complex_workflow() - Test complete user workflow (create, edit, toggle, delete)

# Test Configuration:
# - @pytest.fixture(scope="session", autouse=True) test_services - Start test backend/frontend
# - @pytest.fixture cleanup_todos - Clean todos between tests
# - @pytest.fixture page - Playwright page for each test
# - Use APP_ENV=test for test backend on port 8001
# - Frontend on port 5174 with VITE_API_URL=http://localhost:8001

# Testing Pattern:
# - Use data-testid attributes for element selection
# - Test user interactions (click, type, submit)
# - Verify UI state changes and visual feedback
# - Assert API responses and data persistence
# - Include console error monitoring
# - Test both happy path and edge cases
```

**2. e2e/pyproject.toml - Test Configuration**
```toml
[tool.pytest.ini_options]
baseurl = "http://localhost:5174"
addopts = "-v --tb=short"

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

# Dependencies: pytest, playwright, requests
```

**Playwright Setup:**
```python
# Include proper Playwright configuration:
# - Browser setup (Chromium)
# - Page setup with proper viewport
# - Service management for test backend/frontend
# - Console error capture and reporting
# - Proper cleanup after tests
# - Timeout configuration for reliability
```

IMPORTANT: E2E tests must be reliable (no flakiness), comprehensive (cover all user workflows), and fast (complete in ~10 seconds).
```

---

## 🎯 **Implementation Strategy**

### **Step-by-Step Recreation Process:**

1. **Start with Backend** (Sub-Prompt 1)
   - Implement models, schemas, services, repositories, controllers, main.py
   - Test manually with FastAPI docs at http://localhost:8000/docs

2. **Add Backend Tests** (Sub-Prompt 2) 
   - Create test_api.py with all 12 test cases
   - Verify all tests pass: `pytest test_api.py -v`

3. **Build Frontend** (Sub-Prompt 3)
   - Create services, hooks, components, and main app
   - Test manually at http://localhost:5173

4. **Add E2E Tests** (Sub-Prompt 4)
   - Create comprehensive browser testing
   - Verify all tests pass: `python -m pytest test_todo_e2e.py -v`

### **Success Criteria:**
- ✅ **25 Total Tests Passing** (12 backend + 13 E2E)
- ✅ **Sub-second Backend Tests** (< 1 second execution)
- ✅ **Fast E2E Tests** (< 15 seconds execution)
- ✅ **Professional UI** with Chakra UI business styling
- ✅ **Complete CRUD** operations with error handling
- ✅ **Production Ready** code with proper architecture

### **Testing Commands:**
```bash
# Backend tests (should complete in ~0.5s)
cd backend && pytest test_api.py -v

# E2E tests (should complete in ~10s)  
cd e2e && python -m pytest test_todo_e2e.py -v

# Development servers
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000
cd frontend && npm run dev
```

---

## 🚀 **Usage Instructions**

1. **Copy the Master Prompt** and provide it to Claude Opus 4.1 for project overview
2. **Use Sub-Prompts sequentially** for each implementation phase
3. **Test each phase** before moving to the next
4. **Follow the Step-by-Step Process** for systematic development
5. **Verify Success Criteria** - all 25 tests should pass

This prompt system will recreate a production-ready todo list application with comprehensive testing, professional UI, and clean architecture patterns.

---

*Generated for Claude Opus 4.1 - Professional Full-Stack Development Recreation*