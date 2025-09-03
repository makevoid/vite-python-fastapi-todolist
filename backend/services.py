from typing import List
from schemas import TodoResponse, TodoCreate, TodoUpdate
from repositories import TodoRepository

class TodoService:
    """Service class for todo business logic - uses repository for data access"""

    def __init__(self):
        self.repository = TodoRepository()

    def get_all_todos(self) -> List[TodoResponse]:
        """Get all todos and convert to response models"""
        todos = self.repository.find_all()
        return [TodoResponse.model_validate(todo, from_attributes=True) for todo in todos]

    def get_todo_by_id(self, todo_id: int) -> TodoResponse:
        """Get a specific todo by ID and convert to response model"""
        todo = self.repository.find_by_id(todo_id)
        return TodoResponse.model_validate(todo, from_attributes=True)

    def create_todo(self, todo_data: TodoCreate) -> TodoResponse:
        """Create a new todo from request data"""
        todo = self.repository.create(
            title=todo_data.title,
            description=todo_data.description
        )
        return TodoResponse.model_validate(todo, from_attributes=True)

    def update_todo(self, todo_id: int, update_data: TodoUpdate) -> TodoResponse:
        """Update a todo's details with business logic"""
        todo = self.repository.find_by_id(todo_id)
        
        # Business logic: only update provided fields
        if update_data.title is not None:
            todo.title = update_data.title
        if update_data.description is not None:
            todo.description = update_data.description
        if update_data.completed is not None:
            todo.completed = update_data.completed
        
        updated_todo = self.repository.save(todo)
        return TodoResponse.model_validate(updated_todo, from_attributes=True)

    def toggle_todo_completion(self, todo_id: int) -> TodoResponse:
        """Toggle a todo's completion status (business logic)"""
        todo = self.repository.find_by_id(todo_id)
        todo.completed = not todo.completed
        updated_todo = self.repository.save(todo)
        return TodoResponse.model_validate(updated_todo, from_attributes=True)

    def delete_todo(self, todo_id: int) -> dict:
        """Delete a todo and return success message"""
        self.repository.delete_by_id(todo_id)
        return {"message": f"Todo with id '{todo_id}' deleted"}
