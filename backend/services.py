from typing import List
from peewee import IntegrityError
from models import Counter

class CounterNotFoundException(Exception):
    """Raised when a counter is not found"""
    pass


class CounterAlreadyExistsException(Exception):
    """Raised when trying to create a counter that already exists"""
    pass


class CounterService:
    """Service class for counter business logic"""

    @staticmethod
    def get_all_counters() -> List[Counter]:
        """Get all counters from the database"""
        return list(Counter.select())

    @staticmethod
    def get_counter_by_name(name: str) -> Counter:
        """Get a specific counter by name"""
        try:
            return Counter.get(Counter.name == name)
        except Counter.DoesNotExist:
            raise CounterNotFoundException(f"Counter '{name}' not found")

    @staticmethod
    def create_counter(name: str, initial_value: int = 0) -> Counter:
        """Create a new counter"""
        try:
            return Counter.create(name=name, value=initial_value)
        except IntegrityError:
            raise CounterAlreadyExistsException(f"Counter '{name}' already exists")

    @staticmethod
    def increment_counter(name: str, amount: int = 1) -> Counter:
        """Increment a counter by the specified amount"""
        counter = CounterService.get_counter_by_name(name)
        counter.value += amount
        counter.save()
        return counter

    @staticmethod
    def decrement_counter(name: str, amount: int = 1) -> Counter:
        """Decrement a counter by the specified amount"""
        counter = CounterService.get_counter_by_name(name)
        counter.value -= amount
        counter.save()
        return counter

    @staticmethod
    def reset_counter(name: str) -> Counter:
        """Reset a counter to 0"""
        counter = CounterService.get_counter_by_name(name)
        counter.value = 0
        counter.save()
        return counter

    @staticmethod
    def update_counter(name: str, value: int) -> Counter:
        """Update a counter's value directly"""
        counter = CounterService.get_counter_by_name(name)
        counter.value = value
        counter.save()
        return counter

    @staticmethod
    def delete_counter(name: str) -> bool:
        """Delete a counter"""
        counter = CounterService.get_counter_by_name(name)
        counter.delete_instance()
        return True
