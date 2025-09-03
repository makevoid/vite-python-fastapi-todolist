import pytest
import requests
import subprocess
import time
import os
import signal
import tempfile
from playwright.sync_api import Page, expect, Browser, BrowserContext, Playwright, sync_playwright

# Test environment uses different ports
API_URL = "http://localhost:8001"
APP_URL = "http://localhost:5174"

class TestTodoAppE2E:
    """End-to-end tests for Todo App"""

    @pytest.fixture(scope="session", autouse=True)
    def test_services(self):
        """Start test backend and frontend services for the entire test session"""
        backend_process = None
        frontend_process = None
        
        try:
            # Start test backend on port 8001 using main.py with APP_ENV=test
            env = os.environ.copy()
            env["APP_ENV"] = "test"
            
            backend_process = subprocess.Popen(
                ["python3", "main.py"],
                cwd="../backend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            
            # Wait for backend to start
            for _ in range(30):  # Wait up to 30 seconds
                try:
                    response = requests.get(f"{API_URL}/", timeout=1)
                    if response.status_code == 200:
                        break
                except:
                    time.sleep(1)
            else:
                raise Exception("Backend failed to start")
            
            # Start test frontend on port 5174
            frontend_env = os.environ.copy()
            frontend_env["VITE_API_URL"] = API_URL
            frontend_env["PORT"] = "5174"
            
            frontend_process = subprocess.Popen(
                ["npm", "run", "dev", "--", "--port", "5174"],
                cwd="../frontend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=frontend_env
            )
            
            # Wait for frontend to start
            for _ in range(30):  # Wait up to 30 seconds
                try:
                    response = requests.get(APP_URL, timeout=1)
                    if response.status_code == 200:
                        break
                except:
                    time.sleep(1)
            else:
                raise Exception("Frontend failed to start")
            
            print(f"Test services started: Backend={API_URL}, Frontend={APP_URL}")
            yield
            
        finally:
            # Cleanup processes
            if backend_process:
                backend_process.terminate()
                try:
                    backend_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    backend_process.kill()
            
            if frontend_process:
                frontend_process.terminate()
                try:
                    frontend_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    frontend_process.kill()
            
            # Clean up test database
            test_db_file = os.path.join(tempfile.gettempdir(), "test_todo.db")
            if os.path.exists(test_db_file):
                os.remove(test_db_file)

    @pytest.fixture(scope="session")
    def browser(self):
        """Session-scoped browser instance for speed"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            yield browser
            browser.close()

    @pytest.fixture(scope="session")
    def browser_context(self, browser):
        """Session-scoped browser context for speed"""
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            ignore_https_errors=True
        )
        yield context
        context.close()

    @pytest.fixture(scope="function")  
    def page(self, browser_context):
        """Function-scoped page that reuses the browser context"""
        page = browser_context.new_page()
        # Set shorter default timeouts for speed
        page.set_default_timeout(10000)  # 10s instead of default 30s
        page.set_default_navigation_timeout(10000)  # 10s for navigation
        yield page
        page.close()

    @pytest.fixture(autouse=True)
    def cleanup_todos(self):
        """Clean up todos before each test - optimized for speed"""
        try:
            # Get all todos
            response = requests.get(f"{API_URL}/api/todos", timeout=2)
            if response.ok:
                todos = response.json()
                # Delete each todo with shorter timeout
                for todo in todos:
                    requests.delete(f"{API_URL}/api/todos/{todo['id']}", timeout=1)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            # Backend might not be running or slow
            pass
        yield

    def test_app_title(self, page: Page):
        """Test that the app displays the correct title"""
        page.goto(APP_URL)
        expect(page.locator("h1")).to_contain_text("Todo List App")

    def test_console_errors_on_render(self, page: Page):
        """Test that there are no console errors when rendering the main SPA screen"""
        console_errors = []
        console_warnings = []
        
        # Listen for console messages
        def handle_console_msg(msg):
            if msg.type == 'error':
                console_errors.append(f"Console Error: {msg.text}")
            elif msg.type == 'warning':
                console_warnings.append(f"Console Warning: {msg.text}")
        
        page.on("console", handle_console_msg)
        
        # Navigate to the app
        page.goto(APP_URL)
        
        # Wait for the app to fully load
        expect(page.locator("h1")).to_contain_text("Todo List App")
        
        # Wait briefly for any async errors
        page.wait_for_timeout(500)
        
        # Assert no console errors occurred
        if console_errors:
            error_messages = "\n".join(console_errors)
            raise AssertionError(f"Console errors detected:\n{error_messages}")
        
        # Log warnings for informational purposes (don't fail the test)
        if console_warnings:
            print(f"\nConsole warnings detected (non-fatal):\n" + "\n".join(console_warnings))

    def test_console_errors_during_interactions(self, page: Page):
        """Test that there are no console errors during typical user interactions"""
        console_errors = []
        console_warnings = []
        
        # Listen for console messages
        def handle_console_msg(msg):
            if msg.type == 'error':
                console_errors.append(f"Console Error: {msg.text}")
            elif msg.type == 'warning':
                console_warnings.append(f"Console Warning: {msg.text}")
        
        page.on("console", handle_console_msg)
        
        # Navigate to the app
        page.goto(APP_URL)
        
        # Wait for the app to fully load
        expect(page.locator("h1")).to_contain_text("Todo List App")
        
        # Create a todo
        page.fill('[data-testid="todo-title-input"]', "Test Todo")
        page.fill('[data-testid="todo-description-input"]', "Test description")
        page.click('[data-testid="create-todo-btn"]')
        
        # Wait for todo to appear
        expect(page.locator('[data-testid="todo-1"]')).to_be_visible()
        
        # Perform various todo operations
        page.click('[data-testid="toggle-1"]')  # Toggle completion
        page.click('[data-testid="edit-1"]')    # Start edit
        page.click('[data-testid="cancel-edit-1"]')  # Cancel edit
        page.click('[data-testid="toggle-1"]')  # Toggle back
        
        # Wait for all operations to complete
        page.wait_for_timeout(300)
        
        # Delete the todo
        page.click('[data-testid="delete-1"]')
        
        # Wait briefly for any async errors
        page.wait_for_timeout(300)
        
        # Assert no console errors occurred during interactions
        if console_errors:
            error_messages = "\n".join(console_errors)
            raise AssertionError(f"Console errors detected during interactions:\n{error_messages}")
        
        # Log warnings for informational purposes
        if console_warnings:
            print(f"\nConsole warnings detected during interactions (non-fatal):\n" + "\n".join(console_warnings))

    def test_empty_state(self, page: Page):
        """Test empty state when no todos exist"""
        page.goto(APP_URL)
        expect(page.locator("text=No todos yet")).to_be_visible()

    def test_create_todo(self, page: Page):
        """Test creating a new todo"""
        page.goto(APP_URL)
        
        # Fill in the form
        page.fill('[data-testid="todo-title-input"]', "Buy groceries")
        page.fill('[data-testid="todo-description-input"]', "Milk, bread, eggs")
        
        # Submit the form
        page.click('[data-testid="create-todo-btn"]')
        
        # Wait for the todo to appear
        expect(page.locator('[data-testid="todo-1"]')).to_be_visible()
        
        # Check the todo content
        expect(page.locator('[data-testid="title-1"]')).to_contain_text("Buy groceries")
        expect(page.locator('[data-testid="description-1"]')).to_contain_text("Milk, bread, eggs")

    def test_create_todo_minimal(self, page: Page):
        """Test creating a todo with only title"""
        page.goto(APP_URL)
        
        # Fill only title
        page.fill('[data-testid="todo-title-input"]', "Simple task")
        
        # Submit the form
        page.click('[data-testid="create-todo-btn"]')
        
        # Wait for the todo to appear
        expect(page.locator('[data-testid="todo-1"]')).to_be_visible()
        expect(page.locator('[data-testid="title-1"]')).to_contain_text("Simple task")

    def test_toggle_todo_completion(self, page: Page):
        """Test toggling todo completion status"""
        page.goto(APP_URL)
        
        # Create a todo first
        page.fill('[data-testid="todo-title-input"]', "Complete me")
        page.click('[data-testid="create-todo-btn"]')
        
        # Wait for todo to appear
        expect(page.locator('[data-testid="todo-1"]')).to_be_visible()
        
        # Check initial state (not completed)
        checkbox = page.locator('[data-testid="toggle-1"]')
        expect(checkbox).not_to_be_checked()
        
        # Toggle to completed
        page.click('[data-testid="toggle-1"]')
        expect(checkbox).to_be_checked()
        
        # Toggle back to incomplete
        page.click('[data-testid="toggle-1"]')
        expect(checkbox).not_to_be_checked()

    def test_edit_todo(self, page: Page):
        """Test editing a todo"""
        page.goto(APP_URL)
        
        # Create a todo
        page.fill('[data-testid="todo-title-input"]', "Original Title")
        page.fill('[data-testid="todo-description-input"]', "Original Description")
        page.click('[data-testid="create-todo-btn"]')
        
        expect(page.locator('[data-testid="todo-1"]')).to_be_visible()
        
        # Start editing
        page.click('[data-testid="edit-1"]')
        
        # Edit fields should be visible
        expect(page.locator('[data-testid="edit-title-1"]')).to_be_visible()
        expect(page.locator('[data-testid="edit-description-1"]')).to_be_visible()
        
        # Update values
        page.fill('[data-testid="edit-title-1"]', "Updated Title")
        page.fill('[data-testid="edit-description-1"]', "Updated Description")
        
        # Save changes
        page.click('[data-testid="save-edit-1"]')
        
        # Check updated content
        expect(page.locator('[data-testid="title-1"]')).to_contain_text("Updated Title")
        expect(page.locator('[data-testid="description-1"]')).to_contain_text("Updated Description")

    def test_cancel_edit_todo(self, page: Page):
        """Test canceling todo edit"""
        page.goto(APP_URL)
        
        # Create a todo
        page.fill('[data-testid="todo-title-input"]', "Original Title")
        page.click('[data-testid="create-todo-btn"]')
        
        # Start editing
        page.click('[data-testid="edit-1"]')
        
        # Make changes
        page.fill('[data-testid="edit-title-1"]', "Changed Title")
        
        # Cancel edit
        page.click('[data-testid="cancel-edit-1"]')
        
        # Original content should remain
        expect(page.locator('[data-testid="title-1"]')).to_contain_text("Original Title")

    def test_delete_todo(self, page: Page):
        """Test deleting a todo"""
        page.goto(APP_URL)
        
        # Create a todo
        page.fill('[data-testid="todo-title-input"]', "Delete me")
        page.click('[data-testid="create-todo-btn"]')
        
        expect(page.locator('[data-testid="todo-1"]')).to_be_visible()
        
        # Delete the todo
        page.click('[data-testid="delete-1"]')
        
        # Check the todo is gone
        expect(page.locator('[data-testid="todo-1"]')).not_to_be_visible()
        expect(page.locator("text=No todos yet")).to_be_visible()

    def test_multiple_todos(self, page: Page):
        """Test handling multiple todos"""
        page.goto(APP_URL)
        
        # Create first todo
        page.fill('[data-testid="todo-title-input"]', "First Todo")
        page.click('[data-testid="create-todo-btn"]')
        
        # Create second todo
        page.fill('[data-testid="todo-title-input"]', "Second Todo")
        page.click('[data-testid="create-todo-btn"]')
        
        # Check both todos are visible
        expect(page.locator('[data-testid="todo-1"]')).to_be_visible()
        expect(page.locator('[data-testid="todo-2"]')).to_be_visible()
        
        # Check titles
        expect(page.locator('[data-testid="title-1"]')).to_contain_text("First Todo")
        expect(page.locator('[data-testid="title-2"]')).to_contain_text("Second Todo")
        
        # Toggle completion for first todo
        page.click('[data-testid="toggle-1"]')
        
        # Check badge counts
        expect(page.locator("text=1 Pending")).to_be_visible()
        expect(page.locator("text=1 Done")).to_be_visible()

    def test_todo_persistence_after_refresh(self, page: Page):
        """Test that todos persist after page refresh"""
        page.goto(APP_URL)
        
        # Create todo
        page.fill('[data-testid="todo-title-input"]', "Persistent Todo")
        page.fill('[data-testid="todo-description-input"]', "Should survive refresh")
        page.click('[data-testid="create-todo-btn"]')
        
        # Toggle completion
        page.click('[data-testid="toggle-1"]')
        
        # Refresh the page
        page.reload()
        
        # Check todo is still there with correct state
        expect(page.locator('[data-testid="todo-1"]')).to_be_visible()
        expect(page.locator('[data-testid="title-1"]')).to_contain_text("Persistent Todo")
        expect(page.locator('[data-testid="description-1"]')).to_contain_text("Should survive refresh")
        expect(page.locator('[data-testid="toggle-1"]')).to_be_checked()

    def test_complex_workflow(self, page: Page):
        """Test a complex workflow with multiple operations"""
        page.goto(APP_URL)
        
        # Create multiple todos
        page.fill('[data-testid="todo-title-input"]', "Task 1")
        page.fill('[data-testid="todo-description-input"]', "First task")
        page.click('[data-testid="create-todo-btn"]')
        
        page.fill('[data-testid="todo-title-input"]', "Task 2")
        page.fill('[data-testid="todo-description-input"]', "Second task")
        page.click('[data-testid="create-todo-btn"]')
        
        # Mark first todo as completed
        page.click('[data-testid="toggle-1"]')
        
        # Edit second todo
        page.click('[data-testid="edit-2"]')
        page.fill('[data-testid="edit-title-2"]', "Updated Task 2")
        page.click('[data-testid="save-edit-2"]')
        
        # Check states
        expect(page.locator('[data-testid="toggle-1"]')).to_be_checked()
        expect(page.locator('[data-testid="title-2"]')).to_contain_text("Updated Task 2")
        
        # Check badge counts
        expect(page.locator("text=1 Pending")).to_be_visible()
        expect(page.locator("text=1 Done")).to_be_visible()
        
        # Delete completed todo
        page.click('[data-testid="delete-1"]')
        
        # Only second todo should remain
        expect(page.locator('[data-testid="todo-1"]')).not_to_be_visible()
        expect(page.locator('[data-testid="todo-2"]')).to_be_visible()
        expect(page.locator("text=1 Pending")).to_be_visible()
        expect(page.locator("text=0 Done")).to_be_visible()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])