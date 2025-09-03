from fastapi import HTTPException
from typing import List

from schemas import TodoResponse, TodoCreate, TodoUpdate
from services import TodoService
from repositories import TodoNotFoundException


class TodoController:
    """Controller class for todo API endpoints"""

    def __init__(self):
        self.service = TodoService()

    def get_all_todos(self) -> List[TodoResponse]:
        """Get all todos"""
        return self.service.get_all_todos()

    def get_todo(self, todo_id: int) -> TodoResponse:
        """Get a specific todo by ID"""
        try:
            return self.service.get_todo_by_id(todo_id)
        except TodoNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    def create_todo(self, todo: TodoCreate) -> TodoResponse:
        """Create a new todo"""
        return self.service.create_todo(todo)

    def update_todo(self, todo_id: int, update: TodoUpdate) -> TodoResponse:
        """Update a todo's details"""
        try:
            return self.service.update_todo(todo_id, update)
        except TodoNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    def toggle_todo_completion(self, todo_id: int) -> TodoResponse:
        """Toggle a todo's completion status"""
        try:
            return self.service.toggle_todo_completion(todo_id)
        except TodoNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    def delete_todo(self, todo_id: int) -> dict:
        """Delete a todo"""
        try:
            return self.service.delete_todo(todo_id)
        except TodoNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))
