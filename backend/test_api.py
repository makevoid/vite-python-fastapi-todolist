import pytest
from fastapi.testclient import TestClient
from peewee import SqliteDatabase
from main import app
from models import Todo


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
