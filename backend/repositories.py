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
