from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List

from models import db, Counter
from schemas import CounterResponse, CounterCreate, CounterUpdate, IncrementRequest
from controllers import CounterController

# Lifespan context manager for database
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db.connect()
    db.create_tables([Counter])

    yield

    # Shutdown
    db.close()

# Create FastAPI app
app = FastAPI(title="Counter API", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize controller
counter_controller = CounterController()

# Routes
@app.get("/")
def read_root():
    return {"message": "Counter API", "version": "1.0.0"}

@app.get("/api/counters", response_model=List[CounterResponse])
def get_all_counters():
    """Get all counters"""
    return counter_controller.get_all_counters()

@app.get("/api/counters/{counter_name}", response_model=CounterResponse)
def get_counter(counter_name: str):
    """Get a specific counter by name"""
    return counter_controller.get_counter(counter_name)

@app.post("/api/counters", response_model=CounterResponse)
def create_counter(counter: CounterCreate):
    """Create a new counter"""
    return counter_controller.create_counter(counter)

@app.post("/api/counters/{counter_name}/increment", response_model=CounterResponse)
def increment_counter(counter_name: str, request: IncrementRequest = IncrementRequest()):
    """Increment a counter by a specified amount"""
    return counter_controller.increment_counter(counter_name, request)

@app.post("/api/counters/{counter_name}/decrement", response_model=CounterResponse)
def decrement_counter(counter_name: str, request: IncrementRequest = IncrementRequest()):
    """Decrement a counter by a specified amount"""
    return counter_controller.decrement_counter(counter_name, request)

@app.post("/api/counters/{counter_name}/reset", response_model=CounterResponse)
def reset_counter(counter_name: str):
    """Reset a counter to 0"""
    return counter_controller.reset_counter(counter_name)

@app.put("/api/counters/{counter_name}", response_model=CounterResponse)
def update_counter(counter_name: str, update: CounterUpdate):
    """Update a counter's value directly"""
    return counter_controller.update_counter(counter_name, update)

@app.delete("/api/counters/{counter_name}")
def delete_counter(counter_name: str):
    """Delete a counter"""
    return counter_controller.delete_counter(counter_name)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
