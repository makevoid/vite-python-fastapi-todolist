# Counter App

A professional full-stack counter application built with modern web technologies and object-oriented architecture. This system demonstrates enterprise-level patterns, comprehensive testing, and clean separation of concerns across both frontend and backend.

## 🚀 Features

### Frontend Capabilities
- **Modern UI Design**: Professional business-style interface with Chakra UI v2 components
- **Real-time Updates**: Instant counter modifications with optimistic updates
- **Responsive Design**: Mobile-first approach with consistent styling
- **Error Handling**: Comprehensive error states with user-friendly toast notifications
- **Loading States**: Visual feedback for all operations with proper loading indicators
- **Form Validation**: Input validation with clear error messages
- **Multiple Operations**: Create, increment/decrement (±1, ±10), reset, update, and delete counters

### Backend Capabilities
- **RESTful API**: Full CRUD operations with proper HTTP methods and status codes
- **Data Persistence**: SQLite database with automatic schema management
- **Error Handling**: Structured error responses with detailed messages
- **Data Validation**: Comprehensive input validation using Pydantic models
- **CORS Support**: Cross-origin requests enabled for development and production
- **Auto-documentation**: Swagger/OpenAPI docs automatically generated

### Technical Excellence
- **Object-Oriented Architecture**: Clean separation with services, repositories, and controllers
- **Type Safety**: TypeScript-style patterns in JavaScript with comprehensive JSDoc
- **Modern React**: Hooks-based components with custom hooks for business logic
- **State Management**: TanStack React Query for server state with caching and synchronization
- **Testing Strategy**: Multi-layered testing with unit, integration, and end-to-end tests
- **Development Experience**: Hot reload, auto-restart, and comprehensive error feedback

## 🏗️ Project Structure

### Backend Architecture (Python/FastAPI)

```
backend/
├── main.py              # FastAPI application setup and route definitions
├── models.py            # Database models using Peewee ORM
├── schemas.py           # Pydantic models for request/response validation
├── services.py          # Business logic layer with service classes
├── controllers.py       # HTTP request/response handling layer
├── test_api.py         # Unit and integration tests
└── requirements.txt     # Python dependencies
```

**Object-Oriented Design Patterns:**

- **Service Layer**: `CounterService` handles all business logic operations
- **Repository Pattern**: `CounterRepository` manages data access and response model conversion
- **Controller Layer**: `CounterController` handles HTTP concerns and error translation
- **Custom Exceptions**: Domain-specific exceptions for better error handling
- **Dependency Injection**: Clean separation of concerns with minimal coupling

### Frontend Architecture (React/Vite)

```
frontend/
├── src/
│   ├── App.jsx                    # Main application component
│   ├── main.jsx                   # Application entry point with providers
│   ├── services/
│   │   ├── ApiService.js          # Base HTTP client class
│   │   └── CounterService.js      # Counter-specific API operations
│   ├── hooks/
│   │   └── useCounters.js         # Custom hook for counter operations
│   └── index.css                  # Global styles
├── package.json             # Dependencies and scripts
├── vite.config.js          # Build configuration
└── playwright.config.js    # E2E test configuration
```

**Service-Oriented Design:**

- **Base Service Class**: Generic HTTP operations with error handling
- **Specialized Services**: Domain-specific API operations extending base class
- **Custom Hooks**: React Query integration with service layer abstraction
- **Component Separation**: UI components separated from business logic
- **Type-Safe Operations**: JSDoc annotations for better development experience

### End-to-End Testing

```
e2e/
├── test_counter_e2e.py    # Comprehensive user workflow tests
└── pytest.ini            # Test configuration
```

## 🧪 Testing Strategy & Philosophy

### Why We Test This Way

Our testing strategy follows the **Testing Pyramid** principle with three distinct layers that each serve specific purposes:

#### 1. **Unit Tests** (Backend - `test_api.py`)
**Purpose**: Test individual API endpoints and business logic in isolation.

**What We Test**:
- All CRUD operations (Create, Read, Update, Delete)
- Error handling and edge cases
- Data validation and type checking
- Business rule enforcement
- Database interactions

**Why It Matters**:
- **Fast Feedback**: Unit tests run in milliseconds, providing immediate feedback
- **Isolation**: Each test is independent with in-memory database fixtures
- **Reliability**: Catches bugs early in the development cycle
- **Documentation**: Tests serve as executable documentation of API behavior

**Coverage Goals**:
- ✅ All API endpoints (GET, POST, PUT, DELETE)
- ✅ Success scenarios with valid data
- ✅ Error scenarios (404, 400, validation errors)
- ✅ Edge cases (duplicate names, non-existent counters)
- ✅ Complex workflows combining multiple operations

#### 2. **Integration Tests** (Implicit in E2E)
**Purpose**: Verify that frontend and backend work together correctly.

**What We Test**:
- API communication between frontend and backend
- Data serialization/deserialization
- Cross-origin requests (CORS)
- Authentication and authorization flows (when implemented)

#### 3. **End-to-End Tests** (Playwright - `test_counter_e2e.py`)
**Purpose**: Test complete user workflows from a real user's perspective.

**What We Test**:
- **User Journeys**: Complete workflows that users actually perform
- **Browser Compatibility**: Real browser testing with multiple engines
- **JavaScript Console Monitoring**: Catch runtime errors that unit tests miss
- **Visual Validation**: Ensure UI elements appear and behave correctly
- **Cross-Browser Consistency**: Same behavior across different browsers

**Key Test Scenarios**:
- ✅ **Application Loading**: Verify app loads without console errors
- ✅ **Counter Creation**: Full form submission and validation workflow
- ✅ **Counter Operations**: All increment/decrement/reset operations
- ✅ **Data Persistence**: Verify data survives page refreshes
- ✅ **Error States**: UI properly handles API failures
- ✅ **Complex Workflows**: Multi-step operations that mirror real usage

**Console Error Detection**:
Our E2E tests include specialized console monitoring that catches:
- JavaScript runtime errors during initial page load
- Console errors during user interactions
- Uncaught promise rejections
- Network errors and failed API calls

### Testing Tools & Technologies

- **Backend Testing**: `pytest` with FastAPI TestClient
- **Frontend Testing**: Playwright for cross-browser E2E testing
- **Database Testing**: In-memory SQLite for fast, isolated tests
- **Error Monitoring**: Console error detection during E2E tests
- **Test Data Management**: Automatic cleanup between tests

### Running the Test Suite

```bash
# Backend unit tests
cd backend
pytest test_api.py -v

# End-to-end tests
cd e2e
python3 -m pytest test_counter_e2e.py -v

# Specific test scenarios
pytest test_counter_e2e.py::TestCounterAppE2E::test_console_errors_on_render -v
```

## 🛠️ Development Setup

### Prerequisites
- **Python 3.11+** for backend development
- **Node.js 18+** for frontend development
- **Git** for version control

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vite-python-fastapi-counter
   ```

2. **Start the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Start the frontend** (new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Run tests** (optional)
   ```bash
   # Backend tests
   cd backend && pytest test_api.py -v

   # E2E tests (requires both servers running)
   cd e2e && python3 -m pytest test_counter_e2e.py -v
   ```

### Development URLs
- **Frontend Application**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📚 API Reference

### Base URL
All API endpoints are prefixed with `/api/counters`

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Get all counters |
| `POST` | `/` | Create new counter |
| `GET` | `/{name}` | Get specific counter |
| `PUT` | `/{name}` | Update counter value |
| `DELETE` | `/{name}` | Delete counter |
| `POST` | `/{name}/increment` | Increment counter |
| `POST` | `/{name}/decrement` | Decrement counter |
| `POST` | `/{name}/reset` | Reset counter to 0 |

### Example Requests

**Create Counter**
```json
POST /api/counters
{
  "name": "page-views",
  "initial_value": 0
}
```

**Increment Counter**
```json
POST /api/counters/page-views/increment
{
  "amount": 5
}
```

## 🔧 Development Workflow

### Adding New Features

1. **Backend Changes**:
   - Add Pydantic models to `schemas.py`
   - Implement business logic in `services.py`
   - Add controller methods in `controllers.py`
   - Update routes in `main.py`
   - Write unit tests in `test_api.py`

2. **Frontend Changes**:
   - Add service methods to appropriate service class
   - Update custom hooks for React Query integration
   - Modify UI components as needed
   - Update E2E tests for new functionality

3. **Testing**:
   - Run backend unit tests: `pytest test_api.py -v`
   - Run E2E tests: `python3 -m pytest test_counter_e2e.py -v`
   - Verify console error monitoring passes

### Deployment

**Docker Deployment** (when implemented):
```bash
docker-compose up --build
```

**Manual Deployment**:
1. Build frontend: `npm run build`
2. Deploy backend with production WSGI server
3. Configure reverse proxy for frontend assets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make changes following the existing patterns
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using modern web technologies and clean architecture principles.**

- **Backend (FastAPI + Python)**:
  - RESTful API with full CRUD operations
  - SQLite database with Peewee ORM
  - Comprehensive API documentation (OpenAPI/Swagger)
  - Complete test coverage with pytest

- **Frontend (React + Vite)**:
  - Modern React application with hooks
  - Beautiful, responsive design
  - Real-time counter operations
  - Error handling and loading states

- **Testing**:
  - Unit tests for backend API
  - End-to-end tests with Playwright
  - Multiple browser testing (Chrome, Firefox, Safari)

## Project Structure

```
vite-python-fastapi-counter/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── test_api.py          # Backend tests
│   ├── requirements.txt     # Python dependencies
│   ├── pytest.ini          # Pytest configuration
│   └── Dockerfile           # Docker configuration
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Styles
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Global styles
│   ├── tests/
│   │   └── counter.spec.js  # E2E tests
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── playwright.config.js # Playwright configuration
│   └── Dockerfile           # Docker configuration
└── docker-compose.yml       # Docker Compose setup
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional)

### Option 1: Manual Setup

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Option 2: Docker Setup

```bash
docker-compose up --build
```

## API Endpoints

- `GET /` - API info
- `GET /api/counters` - Get all counters
- `GET /api/counters/{name}` - Get specific counter
- `POST /api/counters` - Create new counter
- `POST /api/counters/{name}/increment` - Increment counter
- `POST /api/counters/{name}/decrement` - Decrement counter
- `POST /api/counters/{name}/reset` - Reset counter to 0
- `PUT /api/counters/{name}` - Update counter value
- `DELETE /api/counters/{name}` - Delete counter

## Testing

### Backend Tests

```bash
cd backend
pytest test_api.py -v
```

### End-to-End Tests

```bash
cd frontend
npm run test:e2e
```

### Interactive Testing

```bash
cd frontend
npm run test:e2e:ui
```

## Development

### Backend Development

The FastAPI backend uses:
- **FastAPI** for the web framework
- **Peewee** as the ORM
- **SQLite** for the database
- **Pydantic** for data validation
- **pytest** for testing

### Frontend Development

The React frontend uses:
- **React 18** with hooks
- **Vite** for build tooling
- **Modern CSS** with responsive design
- **Playwright** for E2E testing

### Testing Strategy

1. **Backend Testing**: Comprehensive unit tests covering all API endpoints, error cases, and database operations
2. **E2E Testing**: Full user workflow testing including UI interactions, API calls, and data persistence

## Features Implemented

- Create counters with custom names and initial values
- Increment/decrement by 1 or 10
- Reset counters to 0
- Set counter values directly
- Delete counters
- Error handling for duplicate names
- Data persistence across page reloads
- Responsive design for mobile/desktop
- Loading states and error messages

## Architecture

- **Clean separation** between frontend and backend
- **RESTful API design** following best practices
- **Modern React patterns** with functional components and hooks
- **Comprehensive error handling** throughout the stack
- **Scalable testing** approach with unit and E2E tests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License
