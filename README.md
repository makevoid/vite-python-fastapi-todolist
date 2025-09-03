# Todo List App

A professional full-stack todo list application built with modern web technologies and object-oriented architecture. This system demonstrates enterprise-level patterns, comprehensive testing, and clean separation of concerns across both frontend and backend.

## 🚀 Features

### Frontend Capabilities
- **Modern UI Design**: Professional business-style interface with Chakra UI v2 components
- **Real-time Updates**: Instant todo modifications with optimistic updates
- **Responsive Design**: Mobile-first approach with consistent styling
- **Error Handling**: Comprehensive error states with user-friendly toast notifications
- **Loading States**: Visual feedback for all operations with proper loading indicators
- **Form Validation**: Input validation with clear error messages
- **Multiple Operations**: Create, update, toggle completion, and delete todos with inline editing

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
├── repositories.py      # Data access layer with repository pattern
├── test_api.py         # Unit and integration tests
└── requirements.txt     # Python dependencies
```

**Object-Oriented Design Patterns:**

- **Service Layer**: `TodoService` handles all business logic operations
- **Repository Pattern**: `TodoRepository` manages data access and response model conversion
- **Controller Layer**: `TodoController` handles HTTP concerns and error translation
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
│   │   └── TodoService.js         # Todo-specific API operations
│   ├── hooks/
│   │   └── useTodos.js            # Custom hook for todo operations
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
├── test_todo_e2e.py    # Comprehensive user workflow tests
└── pyproject.toml      # Test configuration
```

## 🧪 Testing Strategy & Philosophy

### Why We Test This Way

Our testing strategy follows the **Testing Pyramid** principle with three distinct layers that each serve specific purposes:

#### 1. **Unit Tests** (Backend - `test_api.py`)
**Purpose**: Test individual API endpoints and business logic in isolation.

**What We Test**:
- All CRUD operations (Create, Read, Update, Delete)
- Error handling and edge cases
- Data validation and business rules
- Edge cases (duplicate titles, non-existent todos)
- Complex workflows combining multiple operations

**Benefits**:
- ✅ **Fast execution** (typically under 1 second)
- ✅ **Isolated testing** with database reset between tests
- ✅ **Comprehensive coverage** of all API endpoints
- ✅ **Immediate feedback** during development

#### 2. **End-to-End Tests** (Playwright - `test_todo_e2e.py`)
**Purpose**: Test complete user workflows from browser interaction to database persistence.

**What We Test**:
- ✅ **Todo Creation**: Full form submission and validation workflow
- ✅ **Todo Operations**: All completion toggle, edit, and delete operations
- ✅ **UI Interactions**: Real browser interactions with visual validation
- ✅ **Data Persistence**: Verify changes persist across page refreshes
- ✅ **Console Errors**: Monitor for JavaScript errors during interactions
- ✅ **Complex Workflows**: Multi-step user scenarios

**Benefits**:
- ✅ **Real browser testing** with actual user interactions
- ✅ **Full system integration** including database and UI
- ✅ **Visual regression detection** through screenshot comparison
- ✅ **Production-like environment** testing

### Test Coverage Summary
- **Backend Unit Tests**: 12 comprehensive test cases
- **E2E Integration Tests**: 13 user workflow scenarios
- **Error Monitoring**: Console error detection during all interactions
- **Database Testing**: Full CRUD operations with proper cleanup

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Node.js 18+** 
- **npm/yarn**

### 1. Clone & Setup
```bash
git clone <repository-url>
cd vite-python-fastapi-todolist

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup  
cd ../frontend
npm install
```

### 2. Development Mode
```bash
# Terminal 1: Backend (Port 8000)
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend (Port 5173)  
cd frontend
npm run dev
```

### 3. Run Tests
```bash
# Backend unit tests
cd backend
pytest test_api.py -v

# End-to-end tests
cd e2e && python3 -m pytest test_todo_e2e.py -v

# Quick single E2E test
python3 -m pytest test_todo_e2e.py::TestTodoAppE2E::test_app_title -v
```

## 📡 API Reference

All API endpoints are prefixed with `/api/todos`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Get all todos |
| `POST` | `/` | Create new todo |
| `GET` | `/{id}` | Get specific todo |
| `PUT` | `/{id}` | Update todo |
| `POST` | `/{id}/toggle` | Toggle todo completion |
| `DELETE` | `/{id}` | Delete todo |

### Example Requests

**Create Todo**
```bash
POST /api/todos
Content-Type: application/json

{
  "title": "Learn FastAPI",
  "description": "Build a todo app with Python and React"
}
```

**Toggle Todo Completion**
```bash
POST /api/todos/1/toggle
```

## 🔧 Development Workflow

### Day-to-Day Development
1. **Start Services**: Backend (port 8000) + Frontend (port 5173)
2. **Interactive API Docs**: Visit http://localhost:8000/docs for Swagger UI
3. **Hot Reload**: Both services support hot reload for rapid development
4. **Testing**: Run unit tests first, then E2E tests for integration validation

### Key Development URLs
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API docs**: http://localhost:8000/redoc

### Project Structure Overview
```
vite-python-fastapi-todolist/
├── backend/          # FastAPI backend
│   ├── main.py       # App setup & routes
│   ├── models.py     # Database models
│   ├── services.py   # Business logic
│   └── test_api.py   # Unit tests
├── frontend/         # React frontend  
│   ├── src/
│   │   ├── App.jsx   # Main component
│   │   └── services/ # API services
│   └── package.json
├── e2e/             # End-to-end tests
│   └── test_todo_e2e.py
└── README.md
```

## 🎯 Key Features

### Frontend Features
- Professional Chakra UI design with business styling
- Inline editing for todos with save/cancel functionality
- Real-time completion status with visual feedback
- Toast notifications for all operations
- Responsive design for desktop and mobile
- Loading states and error handling

### Backend Features  
- FastAPI with auto-generated OpenAPI documentation
- SQLite database with Peewee ORM
- Full CRUD operations with proper HTTP status codes
- Input validation with Pydantic models
- Structured error responses
- CORS support for frontend integration

### API Endpoints
- `GET /api/todos` - Get all todos
- `GET /api/todos/{id}` - Get specific todo
- `POST /api/todos` - Create new todo
- `PUT /api/todos/{id}` - Update todo
- `POST /api/todos/{id}/toggle` - Toggle completion status
- `DELETE /api/todos/{id}` - Delete todo

### User Experience
- Create todos with title and optional description
- Toggle completion status with checkboxes
- Edit todos inline with dedicated edit mode
- Delete todos with confirmation
- Visual distinction between completed and pending todos
- Progress badges showing completed vs pending todo counts

## 🔬 Technical Implementation

This todo application demonstrates several advanced development patterns:

### Backend Architecture
- **Layered Architecture**: Separation of controllers, services, repositories, and models
- **Repository Pattern**: Data access abstraction with service integration
- **Exception Handling**: Custom exceptions with proper HTTP status mapping
- **ORM Integration**: Peewee ORM with SQLite for simple yet powerful data persistence

### Frontend Architecture  
- **Service Layer**: HTTP client abstraction with TodoService extending ApiService
- **Custom Hooks**: useTodos hook integrating TanStack React Query with services
- **State Management**: Server state management with optimistic updates
- **Component Design**: Professional UI components with consistent styling

### Testing Strategy
- **Unit Testing**: Backend API testing with pytest and test database isolation
- **E2E Testing**: Full user workflow testing with Playwright
- **Error Monitoring**: Console error detection during browser interactions
- **Test Isolation**: Proper cleanup and setup for reliable test execution

## 📝 Contributing

1. **Development Setup**: Follow the Quick Start guide
2. **Testing**: Ensure all tests pass before submitting changes
   - Run backend tests: `pytest test_api.py -v`
   - Run E2E tests: `python3 -m pytest test_todo_e2e.py -v`
3. **Code Style**: Follow existing patterns and maintain consistent formatting
4. **Documentation**: Update README if adding new features or changing APIs

This todo application serves as a comprehensive example of modern full-stack development with professional patterns, thorough testing, and clean architecture.