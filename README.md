# 📝 Todo List App

<div align="center">

![Tests](https://img.shields.io/badge/Tests-25%20Passing-success?style=for-the-badge)
<!-- insert other badges here -->

**A full-stack todo list app repo template to kickstart any of your projects**

*Built with FastAPI + React Vite, JSX + Comprehensive Integration Testing*

Iterate from a todo list to any app. Use this repo as a base.

</div>

---

### 🤖 **Quick Start with AI Coding Assistants**

**Ready to build your custom app?** This todo app serves as a foundation that can be transformed into any application you want to build.

#### Option 1: Use This Repository
1. **Open your AI coding environment** (Claude Code, Cursor, GitHub Copilot, or any AI assistant)
2. **Run the setup command:** Ask your AI assistant to run: `install and run the project`
3. **Wait for setup completion:** The AI will install all packages and run tests automatically
4. **Environment ready:** Once tests pass, your AI coding environment is ready
5. **Transform the app:** Give your AI assistant a prompt like: "Transform this todo app into a [task management system / expense tracker / inventory manager / etc.]"

#### Option 2: Use Just the Prompt (No Repository Needed)
**Don't want to clone this repo?** Use our standalone prompt instead:

1. **Copy the [docs/PROMPT.md](./docs/PROMPT.md) file** - Contains complete specifications for recreating this app
2. **Paste into any AI assistant** - Works with Claude, ChatGPT, Cursor, GitHub Copilot, etc.
3. **AI builds everything from scratch** - Creates the entire full-stack app based on the prompt
4. **Customize during creation** - Tell the AI to modify it for your specific use case while building

**What is PROMPT.md?** It's a comprehensive specification document that describes exactly how to build this entire application. Any AI assistant can use it to recreate the full codebase, tests, and documentation from scratch - no repository needed!

The AI will handle all setup, testing, and troubleshooting automatically with either approach!

---

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

### End-to-End Testing

```
e2e/
├── test_todo_e2e.py    # Comprehensive user workflow tests
└── pyproject.toml      # Test configuration
```

## 🚀 Quick Start

<div align="center">

### ⚡ **Get Running in 60 Seconds**

</div>

### Prerequisites
- **Python 3.11+** 🐍
- **Node.js 18+** 📦 
- **npm/yarn** ⚙️

### 1. Clone & Setup
```bash
git clone <repository-url>
cd vite-python-fastapi-todolist

# Backend setup 🐍
cd backend
pip install -r requirements.txt

# Frontend setup ⚛️
cd ../frontend
npm install
```

### 2. Development Mode
```bash
# Terminal 1: Backend (Port 8000) 🚀
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend (Port 5173) ⚡
cd frontend
npm run dev
```

### 3. Run Tests 🧪
```bash
# 🔬 Backend unit tests (12 tests, 0.45s)
cd backend
pytest test_api.py -v

# 🌐 End-to-end tests (13 tests, 10.4s)
cd e2e && python3 -m pytest test_todo_e2e.py -v

# ⚡ Quick smoke test
python3 -m pytest test_todo_e2e.py::TestTodoAppE2E::test_app_title -v
```

<div align="center">

### 🎉 **That's it! Your todo app is live!**

**Frontend**: http://localhost:5173 | **API**: http://localhost:8000 | **Docs**: http://localhost:8000/docs

</div>

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

---

Iterate from a todo list to any app. Use this repo as a base.
