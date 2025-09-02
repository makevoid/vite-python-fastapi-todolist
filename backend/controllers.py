from fastapi import HTTPException
from typing import List

from schemas import CounterResponse, CounterCreate, CounterUpdate, IncrementRequest
from repositories import CounterRepository
from services import CounterNotFoundException, CounterAlreadyExistsException


class CounterController:
    """Controller class for counter API endpoints"""

    def __init__(self):
        self.repository = CounterRepository()

    def get_all_counters(self) -> List[CounterResponse]:
        """Get all counters"""
        return self.repository.find_all()

    def get_counter(self, counter_name: str) -> CounterResponse:
        """Get a specific counter by name"""
        try:
            return self.repository.find_by_name(counter_name)
        except CounterNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    def create_counter(self, counter: CounterCreate) -> CounterResponse:
        """Create a new counter"""
        try:
            return self.repository.create(counter)
        except CounterAlreadyExistsException as e:
            raise HTTPException(status_code=400, detail=str(e))

    def increment_counter(self, counter_name: str, request: IncrementRequest) -> CounterResponse:
        """Increment a counter by a specified amount"""
        try:
            return self.repository.increment(counter_name, request)
        except CounterNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    def decrement_counter(self, counter_name: str, request: IncrementRequest) -> CounterResponse:
        """Decrement a counter by a specified amount"""
        try:
            return self.repository.decrement(counter_name, request)
        except CounterNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    def reset_counter(self, counter_name: str) -> CounterResponse:
        """Reset a counter to 0"""
        try:
            return self.repository.reset(counter_name)
        except CounterNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    def update_counter(self, counter_name: str, update: CounterUpdate) -> CounterResponse:
        """Update a counter's value directly"""
        try:
            return self.repository.update(counter_name, update)
        except CounterNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    def delete_counter(self, counter_name: str) -> dict:
        """Delete a counter"""
        try:
            return self.repository.delete(counter_name)
        except CounterNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))
