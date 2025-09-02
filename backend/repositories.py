from typing import List
from schemas import CounterResponse, CounterCreate, CounterUpdate, IncrementRequest
from services import CounterService

class CounterRepository:
    """Repository pattern for counter data access"""

    def __init__(self):
        self.service = CounterService()

    def find_all(self) -> List[CounterResponse]:
        """Find all counters and return as response models"""
        counters = self.service.get_all_counters()
        return [CounterResponse.model_validate(c, from_attributes=True) for c in counters]

    def find_by_name(self, name: str) -> CounterResponse:
        """Find counter by name and return as response model"""
        counter = self.service.get_counter_by_name(name)
        return CounterResponse.model_validate(counter, from_attributes=True)

    def create(self, counter_data: CounterCreate) -> CounterResponse:
        """Create a new counter from request data"""
        counter = self.service.create_counter(
            name=counter_data.name,
            initial_value=counter_data.initial_value
        )
        return CounterResponse.model_validate(counter, from_attributes=True)

    def increment(self, name: str, request: IncrementRequest) -> CounterResponse:
        """Increment counter and return response model"""
        counter = self.service.increment_counter(name, request.amount)
        return CounterResponse.model_validate(counter, from_attributes=True)

    def decrement(self, name: str, request: IncrementRequest) -> CounterResponse:
        """Decrement counter and return response model"""
        counter = self.service.decrement_counter(name, request.amount)
        return CounterResponse.model_validate(counter, from_attributes=True)

    def reset(self, name: str) -> CounterResponse:
        """Reset counter and return response model"""
        counter = self.service.reset_counter(name)
        return CounterResponse.model_validate(counter, from_attributes=True)

    def update(self, name: str, update_data: CounterUpdate) -> CounterResponse:
        """Update counter and return response model"""
        counter = self.service.update_counter(name, update_data.value)
        return CounterResponse.model_validate(counter, from_attributes=True)

    def delete(self, name: str) -> dict:
        """Delete counter and return success message"""
        self.service.delete_counter(name)
        return {"message": f"Counter '{name}' deleted"}
