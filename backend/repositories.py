from typing import List
from models import Todo

class TodoNotFoundException(Exception):
    """Raised when a todo is not found"""
    pass

class TodoRepository:
    """Repository pattern for todo data access - handles database operations"""

    @staticmethod
    def find_all() -> List[Todo]:
        """Find all todos from the database"""
        return list(Todo.select())

    @staticmethod
    def find_by_id(todo_id: int) -> Todo:
        """Find a todo by ID"""
        try:
            return Todo.get(Todo.id == todo_id)
        except Todo.DoesNotExist:
            raise TodoNotFoundException(f"Todo with id '{todo_id}' not found")

    @staticmethod
    def create(title: str, description: str = '') -> Todo:
        """Create a new todo in the database"""
        return Todo.create(title=title, description=description)

    @staticmethod
    def save(todo: Todo) -> Todo:
        """Save a todo to the database"""
        todo.save()
        return todo

    @staticmethod
    def delete_by_id(todo_id: int) -> bool:
        """Delete a todo by ID"""
        todo = TodoRepository.find_by_id(todo_id)
        todo.delete_instance()
        return True
