import pytest
from fastapi.testclient import TestClient
from peewee import SqliteDatabase
from main import app
from models import Counter


@pytest.fixture(scope="function", autouse=True)
def test_db():
    """Reset database before each test"""
    from models import Counter, db
    
    # Ensure we're connected
    if db.is_closed():
        db.connect()
    
    # Drop and recreate tables to start fresh
    db.drop_tables([Counter], safe=True)
    db.create_tables([Counter])
    
    yield db
    
    # Clean up after test
    db.drop_tables([Counter], safe=True)


@pytest.fixture
def client(test_db):
    """Create a test client using the main app"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def setup_counters():
    """Setup initial test counters using Peewee directly"""
    Counter.create(name="test_counter", value=10)
    Counter.create(name="another_counter", value=5)
    return [
        {"name": "test_counter", "value": 10},
        {"name": "another_counter", "value": 5}
    ]


def test_read_root(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Counter API", "version": "1.0.0"}


def test_get_all_counters_empty(client):
    """Test getting all counters when none exist"""
    response = client.get("/api/counters")
    assert response.status_code == 200
    assert response.json() == []


def test_create_counter(client):
    """Test creating a new counter"""
    response = client.post(
        "/api/counters",
        json={"name": "new_counter", "initial_value": 42}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "new_counter"
    assert data["value"] == 42


def test_get_all_counters(client, setup_counters):
    """Test getting all counters"""
    response = client.get("/api/counters")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Verify counter values
    counter_names = {c["name"]: c["value"] for c in data}
    assert counter_names["test_counter"] == 10
    assert counter_names["another_counter"] == 5


def test_increment_counter(client, setup_counters):
    """Test incrementing a counter"""
    response = client.post(
        "/api/counters/test_counter/increment",
        json={"amount": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["value"] == 15


def test_decrement_counter(client, setup_counters):
    """Test decrementing a counter"""
    response = client.post(
        "/api/counters/test_counter/decrement",
        json={"amount": 3}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["value"] == 7


def test_reset_counter(client, setup_counters):
    """Test resetting a counter"""
    response = client.post("/api/counters/test_counter/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["value"] == 0


def test_update_counter(client, setup_counters):
    """Test updating a counter value directly"""
    response = client.put(
        "/api/counters/test_counter",
        json={"value": 99}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["value"] == 99


def test_get_counter(client, setup_counters):
    """Test getting a specific counter"""
    response = client.get("/api/counters/test_counter")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test_counter"
    assert data["value"] == 10


def test_delete_counter(client, setup_counters):
    """Test deleting a counter"""
    response = client.delete("/api/counters/test_counter")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

    # Verify counter is deleted
    response = client.get("/api/counters/test_counter")
    assert response.status_code == 404


def test_counter_not_found(client):
    """Test operations on non-existent counter"""
    response = client.get("/api/counters/nonexistent")
    assert response.status_code == 404

    response = client.post("/api/counters/nonexistent/increment")
    assert response.status_code == 404


def test_duplicate_counter_creation(client):
    """Test creating a counter with duplicate name"""
    # Create first counter
    client.post("/api/counters", json={"name": "duplicate", "initial_value": 1})

    # Try to create duplicate
    response = client.post("/api/counters", json={"name": "duplicate", "initial_value": 2})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_complex_workflow(client):
    """Test a complex workflow with multiple operations"""
    # Create counter
    response = client.post(
        "/api/counters",
        json={"name": "workflow_counter", "initial_value": 10}
    )
    assert response.status_code == 200

    # Increment
    response = client.post(
        "/api/counters/workflow_counter/increment",
        json={"amount": 5}
    )
    assert response.json()["value"] == 15

    # Decrement
    response = client.post(
        "/api/counters/workflow_counter/decrement",
        json={"amount": 3}
    )
    assert response.json()["value"] == 12

    # Reset
    response = client.post("/api/counters/workflow_counter/reset")
    assert response.json()["value"] == 0

    # Update directly
    response = client.put(
        "/api/counters/workflow_counter",
        json={"value": 50}
    )
    assert response.json()["value"] == 50

    # Delete
    response = client.delete("/api/counters/workflow_counter")
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
