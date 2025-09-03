# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack todo list application with a React frontend, FastAPI backend, and comprehensive testing suite. The architecture follows a clean separation between frontend (React + Vite + Chakra UI) and backend (FastAPI + Peewee ORM + SQLite).

## Development Commands

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000  # Development server
python main.py                                        # Alternative startup
pytest test_api.py -v                                # Run all backend tests
pytest test_api.py::TestTodoAPI::test_create_todo -v # Single test
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev        # Development server (port 5173)
npm run build      # Production build
npm run preview    # Preview production build
```

### End-to-End Testing
```bash
cd e2e
python3 -m pytest test_todo_e2e.py -v                    # All E2E tests
python3 -m pytest test_todo_e2e.py::TestTodoAppE2E::test_app_title -v  # Single E2E test
```

### Docker Development
```bash
docker-compose up --build  # Full stack with containers
docker-compose down        # Stop all services
```

## Architecture and Code Structure

### Backend Architecture (Object-Oriented Design)
The backend follows a clean OOP architecture with separation of concerns:

**Layer Structure:**
- **Controllers** (`controllers.py`): Handle HTTP requests/responses and coordinate with services
- **Services** (`services.py`): Business logic layer with TodoService for operations
- **Repository** (`repositories.py`): Data access layer with TodoRepository pattern
- **Models** (`models.py`): Database models using Peewee ORM
- **Schemas** (`schemas.py`): Pydantic models for request/response validation
- **Main** (`main.py`): FastAPI app configuration and route definitions

**Key Classes:**
- `TodoService`: Static methods for all todo business operations
- `TodoRepository`: Repository pattern with service integration and response model conversion
- `TodoController`: Handles HTTP layer concerns and error translation
- Custom exceptions: `TodoNotFoundException`

### Frontend Architecture (Service-Oriented Design)
React application with service layer and custom hooks:

**Service Layer:**
- `ApiService` (base class): Generic HTTP client with GET/POST/PUT/DELETE methods
- `TodoService`: Extends ApiService with todo-specific operations
- `useTodos` hook: React Query integration with service layer

**Components:**
- **State Management**: Custom hooks with TanStack React Query for server state
- **UI Library**: Chakra UI v2 components with business-style theme
- **HTTP Client**: Class-based service layer abstracting fetch API
- **Styling**: Professional business theme with consistent gray/blue palette
- **Data Fetching**: Service classes integrated with React Query hooks

### Data Flow Pattern (OOP Implementation)
1. User interaction → React component → useTodos hook
2. Hook calls TodoService method → HTTP request via ApiService base class
3. FastAPI route → TodoController → TodoRepository → TodoService
4. TodoService → Peewee ORM → SQLite database
5. Response models via TodoRepository → JSON → React Query cache → UI update

### Testing Strategy
- **Backend**: Unit tests with pytest, covers all API endpoints and edge cases
- **E2E**: Playwright tests for complete user workflows
- **Test Isolation**: Each test cleans up data, uses fixtures for setup

## Configuration Notes

### Environment Variables
- **Frontend**: `VITE_API_URL` (defaults to http://localhost:8000)
- **Development**: Backend runs on :8000, frontend on :5173
- **Production**: Uses Docker containers with proper networking

### Database
- **Development**: SQLite file `todo.db` in backend directory
- **Testing**: In-memory SQLite database for isolation
- **Model**: Single `Todo` table with id, title, description, completed fields

### Development Proxy
Vite configured to proxy `/api/*` requests to backend during development, enabling seamless full-stack development.

## Key Development Patterns

### Error Handling
- **Backend**: FastAPI automatic error responses with proper HTTP status codes
- **Frontend**: Centralized error state with toast notifications using Chakra UI
- **Validation**: Pydantic models ensure data integrity

### API Integration (OOP Service Layer)
Follow the established service patterns:

**Service Class Usage:**
```javascript
// services/TodoService.js
class TodoService extends ApiService {
  async createTodo(title, description = '') {
    return this.post(this.basePath, { title, description });
  }
  
  async updateTodo(id, updates) {
    return this.put(`${this.basePath}/${id}`, updates);
  }
  
  async toggleTodoCompletion(id) {
    return this.post(`${this.basePath}/${id}/toggle`);
  }
}
```

**Custom Hook Integration:**
```javascript
// hooks/useTodos.js
const useTodos = () => {
  const todoService = new TodoService();
  
  const todosQuery = useQuery({
    queryKey: ['todos'],
    queryFn: () => todoService.fetchTodos(),
  });
  
  const createTodoMutation = useMutation({
    mutationFn: ({ title, description }) => todoService.createTodo(title, description),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
  });
  
  const toggleCompletionMutation = useMutation({
    mutationFn: (id) => todoService.toggleTodoCompletion(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
  });
  
  return { 
    todos: todosQuery.data || [],
    createTodo: createTodoMutation.mutate,
    toggleTodoCompletion: toggleCompletionMutation.mutate,
    isCreating: createTodoMutation.isPending,
    isToggling: toggleCompletionMutation.isPending
  };
};
```

**Component Usage:**
```javascript
// App.jsx
const { todos, createTodo, toggleTodoCompletion, isCreating } = useTodos();

const handleSubmit = () => {
  createTodo({ title: todoTitle, description: todoDescription });
};

const handleToggle = (id) => {
  toggleTodoCompletion(id);
};
```

### Testing Patterns
- **Backend tests**: Use `test_db` and `client` fixtures, test all CRUD operations and error cases
- **E2E tests**: Use `cleanup_todos` fixture, test complete user workflows with data-testid selectors
- **Console error testing**: Playwright tests monitor browser console for JavaScript errors during render and interactions
- **Test data**: Always clean up between tests to ensure isolation

## Component and Styling Guidelines

### Chakra UI Usage
- Use Chakra UI v2 components consistently
- Follow established color scheme: blue for primary actions, green for completion, red for deletion
- Maintain responsive design with Chakra's responsive props
- Use proper semantic HTML with ARIA labels for accessibility

### Component Structure
Todo components follow this pattern:
- Card container with shadow and border radius
- Checkbox for completion status
- Todo title and description with conditional styling
- Action buttons (edit/delete) positioned to the right
- Inline editing with save/cancel functionality
- Visual indicators for completed vs pending todos

## Development Workflow

1. **Start Services**: Run backend (port 8000) and frontend (port 5173) simultaneously
2. **API Development**: Use FastAPI auto-generated docs at http://localhost:8000/docs
3. **Testing**: Run backend tests first, then E2E tests to verify integration
4. **Database Changes**: Modify models in `backend/models.py`, restart backend to recreate DB
5. **Frontend Changes**: Vite hot reload handles most changes automatically

## Common Tasks

### Adding New API Endpoints (OOP Pattern)
1. Add Pydantic models to `schemas.py`
2. Add business logic methods to TodoService in `services.py`
3. Add repository methods to TodoRepository in `repositories.py`
4. Add controller methods to TodoController in `controllers.py`
5. Add route handlers in `main.py` that delegate to controllers
6. Add frontend service methods to TodoService class
7. Update useTodos hook to integrate new service methods
8. Write unit tests covering success and error cases

### Debugging Issues
- **Backend logs**: Check uvicorn output for API errors
- **Frontend errors**: Browser console shows React errors and API failures
- **Database issues**: Check `todo.db` file exists and has proper schema
- **Port conflicts**: Ensure ports 5173 (frontend) and 8000 (backend) are available

### Running Tests in CI/CD
Both test suites are designed for CI environments:
- Backend tests use in-memory database (no file dependencies)
- E2E tests can run headless with `--headed` flag for debugging
- All tests include proper cleanup and isolation

## Todo-Specific Features

### Todo Management Operations
- **Create**: Add new todos with title and optional description
- **Read**: Fetch all todos with completion status
- **Update**: Edit todo title, description, or completion status
- **Delete**: Remove todos from the list
- **Toggle**: Quick completion status toggle

### Todo UI Features
- **Visual States**: Completed todos are visually distinct (strikethrough, muted colors)
- **Inline Editing**: Click edit button to modify todos in place
- **Completion Tracking**: Badge displays show pending vs completed todos
- **Responsive Design**: Works on desktop and mobile devices
- **Toast Notifications**: User feedback for all operations

### Todo Data Model
```python
class Todo(Model):
    id = AutoField()           # Primary key
    title = CharField()        # Required todo title
    description = TextField(default='')  # Optional description
    completed = BooleanField(default=False)  # Completion status
```