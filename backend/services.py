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
