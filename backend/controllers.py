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
