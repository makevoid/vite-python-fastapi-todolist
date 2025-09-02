"""
Test version of main.py that uses a separate test database and runs on different ports
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from peewee import SqliteDatabase
import os
import tempfile

# Create test database in temp directory
test_db_file = os.path.join(tempfile.gettempdir(), "test_counter.db")
test_db = SqliteDatabase(test_db_file)

# Import and configure models for test database
from models import Counter
Counter._meta.database = test_db

# Import other modules
from controllers import CounterController
from schemas import CounterCreate, CounterResponse, CounterUpdate, IncrementRequest

app = FastAPI(title="Counter API - Test", version="1.0.0")

# Configure CORS for test
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # Different port for test frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize test database
def init_test_db():
    if test_db.is_closed():
        test_db.connect()
    test_db.create_tables([Counter], safe=True)

# Initialize controller
controller = CounterController()

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Counter API - Test", "version": "1.0.0"}

# Counter endpoints
@app.get("/api/counters", response_model=list[CounterResponse])
async def get_counters():
    return controller.get_all_counters()

@app.post("/api/counters", response_model=CounterResponse)
async def create_counter(counter: CounterCreate):
    return controller.create_counter(counter)

@app.get("/api/counters/{name}", response_model=CounterResponse)
async def get_counter(name: str):
    return controller.get_counter(name)

@app.put("/api/counters/{name}", response_model=CounterResponse)
async def update_counter(name: str, counter_update: CounterUpdate):
    return controller.update_counter(name, counter_update)

@app.delete("/api/counters/{name}")
async def delete_counter(name: str):
    return controller.delete_counter(name)

@app.post("/api/counters/{name}/increment", response_model=CounterResponse)
async def increment_counter(name: str, request: IncrementRequest = IncrementRequest()):
    return controller.increment_counter(name, request)

@app.post("/api/counters/{name}/decrement", response_model=CounterResponse)
async def decrement_counter(name: str, request: IncrementRequest = IncrementRequest()):
    return controller.decrement_counter(name, request)

@app.post("/api/counters/{name}/reset", response_model=CounterResponse)
async def reset_counter(name: str):
    return controller.reset_counter(name)

# Startup event
@app.on_event("startup")
async def startup_event():
    init_test_db()

if __name__ == "__main__":
    init_test_db()
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Different port for test backend