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

class TestCounterAppE2E:
    """End-to-end tests for Counter App"""

    @pytest.fixture(scope="session", autouse=True)
    def test_services(self):
        """Start test backend and frontend services for the entire test session"""
        backend_process = None
        frontend_process = None
        
        try:
            # Start test backend on port 8001
            backend_process = subprocess.Popen(
                ["python3", "test_main.py"],
                cwd="../backend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
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
            env = os.environ.copy()
            env["VITE_API_URL"] = API_URL
            env["PORT"] = "5174"
            
            frontend_process = subprocess.Popen(
                ["npm", "run", "dev", "--", "--port", "5174"],
                cwd="../frontend",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
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
            test_db_file = os.path.join(tempfile.gettempdir(), "test_counter.db")
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
    def cleanup_counters(self):
        """Clean up counters before each test - optimized for speed"""
        try:
            # Get all counters
            response = requests.get(f"{API_URL}/api/counters", timeout=2)
            if response.ok:
                counters = response.json()
                # Delete each counter with shorter timeout
                for counter in counters:
                    requests.delete(f"{API_URL}/api/counters/{counter['name']}", timeout=1)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            # Backend might not be running or slow
            pass
        yield

    def test_app_title(self, page: Page):
        """Test that the app displays the correct title"""
        page.goto(APP_URL)
        expect(page.locator("h1")).to_contain_text("Counter App")

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
        expect(page.locator("h1")).to_contain_text("Counter App")
        
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
        expect(page.locator("h1")).to_contain_text("Counter App")
        
        # Create a counter
        page.fill('[data-testid="counter-name-input"]', "test-counter")
        page.fill('[data-testid="counter-value-input"]', "5")
        page.click('[data-testid="create-counter-btn"]')
        
        # Wait for counter to appear
        expect(page.locator('[data-testid="counter-test-counter"]')).to_be_visible()
        
        # Perform various counter operations
        page.click('[data-testid="increment-test-counter"]')
        page.click('[data-testid="decrement-test-counter"]')
        page.click('[data-testid="increment-10-test-counter"]')
        page.click('[data-testid="reset-test-counter"]')
        
        # Test direct value setting
        page.fill('[data-testid="set-value-test-counter"]', "100")
        page.press('[data-testid="set-value-test-counter"]', "Enter")
        
        # Wait for all operations to complete
        page.wait_for_timeout(300)
        
        # Delete the counter
        page.click('[data-testid="delete-test-counter"]')
        
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
        """Test empty state when no counters exist"""
        page.goto(APP_URL)
        expect(page.locator("text=No counters configured")).to_be_visible()

    def test_create_counter(self, page: Page):
        """Test creating a new counter"""
        page.goto(APP_URL)
        
        # Fill in the form
        page.fill('[data-testid="counter-name-input"]', "test-counter")
        page.fill('[data-testid="counter-value-input"]', "10")
        
        # Submit the form
        page.click('[data-testid="create-counter-btn"]')
        
        # Wait for the counter to appear
        expect(page.locator('[data-testid="counter-test-counter"]')).to_be_visible()
        
        # Check the counter value
        expect(page.locator('[data-testid="value-test-counter"]')).to_contain_text("10")

    def test_increment_counter_by_1(self, page: Page):
        """Test incrementing counter by 1"""
        page.goto(APP_URL)
        
        # Create a counter first
        page.fill('[data-testid="counter-name-input"]', "increment-test")
        page.fill('[data-testid="counter-value-input"]', "5")
        page.click('[data-testid="create-counter-btn"]')
        
        # Wait for counter to appear
        expect(page.locator('[data-testid="counter-increment-test"]')).to_be_visible()
        
        # Increment by 1
        page.click('[data-testid="increment-increment-test"]')
        
        # Check the new value
        expect(page.locator('[data-testid="value-increment-test"]')).to_contain_text("6")

    def test_increment_counter_by_10(self, page: Page):
        """Test incrementing counter by 10"""
        page.goto(APP_URL)
        
        # Create a counter
        page.fill('[data-testid="counter-name-input"]', "big-increment")
        page.fill('[data-testid="counter-value-input"]', "20")
        page.click('[data-testid="create-counter-btn"]')
        
        expect(page.locator('[data-testid="counter-big-increment"]')).to_be_visible()
        
        # Increment by 10
        page.click('[data-testid="increment-10-big-increment"]')
        
        # Check the new value
        expect(page.locator('[data-testid="value-big-increment"]')).to_contain_text("30")

    def test_decrement_counter_by_1(self, page: Page):
        """Test decrementing counter by 1"""
        page.goto(APP_URL)
        
        # Create a counter
        page.fill('[data-testid="counter-name-input"]', "decrement-test")
        page.fill('[data-testid="counter-value-input"]', "15")
        page.click('[data-testid="create-counter-btn"]')
        
        expect(page.locator('[data-testid="counter-decrement-test"]')).to_be_visible()
        
        # Decrement by 1
        page.click('[data-testid="decrement-decrement-test"]')
        
        # Check the new value
        expect(page.locator('[data-testid="value-decrement-test"]')).to_contain_text("14")

    def test_decrement_counter_by_10(self, page: Page):
        """Test decrementing counter by 10"""
        page.goto(APP_URL)
        
        # Create a counter
        page.fill('[data-testid="counter-name-input"]', "big-decrement")
        page.fill('[data-testid="counter-value-input"]', "50")
        page.click('[data-testid="create-counter-btn"]')
        
        expect(page.locator('[data-testid="counter-big-decrement"]')).to_be_visible()
        
        # Decrement by 10
        page.click('[data-testid="decrement-10-big-decrement"]')
        
        # Check the new value
        expect(page.locator('[data-testid="value-big-decrement"]')).to_contain_text("40")

    def test_reset_counter(self, page: Page):
        """Test resetting a counter to 0"""
        page.goto(APP_URL)
        
        # Create a counter
        page.fill('[data-testid="counter-name-input"]', "reset-test")
        page.fill('[data-testid="counter-value-input"]', "99")
        page.click('[data-testid="create-counter-btn"]')
        
        expect(page.locator('[data-testid="counter-reset-test"]')).to_be_visible()
        
        # Reset the counter
        page.click('[data-testid="reset-reset-test"]')
        
        # Check the value is 0
        expect(page.locator('[data-testid="value-reset-test"]')).to_contain_text("0")

    def test_delete_counter(self, page: Page):
        """Test deleting a counter"""
        page.goto(APP_URL)
        
        # Create a counter
        page.fill('[data-testid="counter-name-input"]', "delete-test")
        page.fill('[data-testid="counter-value-input"]', "42")
        page.click('[data-testid="create-counter-btn"]')
        
        expect(page.locator('[data-testid="counter-delete-test"]')).to_be_visible()
        
        # Delete the counter
        page.click('[data-testid="delete-delete-test"]')
        
        # Check the counter is gone
        expect(page.locator('[data-testid="counter-delete-test"]')).not_to_be_visible()
        expect(page.locator("text=No counters configured")).to_be_visible()

    def test_set_counter_value_directly(self, page: Page):
        """Test setting counter value directly"""
        page.goto(APP_URL)
        
        # Create a counter
        page.fill('[data-testid="counter-name-input"]', "set-value-test")
        page.fill('[data-testid="counter-value-input"]', "10")
        page.click('[data-testid="create-counter-btn"]')
        
        expect(page.locator('[data-testid="counter-set-value-test"]')).to_be_visible()
        
        # Set a new value
        input_field = page.locator('[data-testid="set-value-set-value-test"]')
        input_field.fill("123")
        input_field.press("Enter")
        
        # Check the new value
        expect(page.locator('[data-testid="value-set-value-test"]')).to_contain_text("123")

    def test_multiple_counters(self, page: Page):
        """Test handling multiple counters"""
        page.goto(APP_URL)
        
        # Create first counter
        page.fill('[data-testid="counter-name-input"]', "counter-1")
        page.fill('[data-testid="counter-value-input"]', "10")
        page.click('[data-testid="create-counter-btn"]')
        
        # Create second counter
        page.fill('[data-testid="counter-name-input"]', "counter-2")
        page.fill('[data-testid="counter-value-input"]', "20")
        page.click('[data-testid="create-counter-btn"]')
        
        # Check all counters are visible
        expect(page.locator('[data-testid="counter-counter-1"]')).to_be_visible()
        expect(page.locator('[data-testid="counter-counter-2"]')).to_be_visible()
        
        # Check values
        expect(page.locator('[data-testid="value-counter-1"]')).to_contain_text("10")
        expect(page.locator('[data-testid="value-counter-2"]')).to_contain_text("20")
        
        # Modify each counter differently
        page.click('[data-testid="increment-counter-1"]')
        page.click('[data-testid="decrement-counter-2"]')
        
        # Check updated values
        expect(page.locator('[data-testid="value-counter-1"]')).to_contain_text("11")
        expect(page.locator('[data-testid="value-counter-2"]')).to_contain_text("19")

    def test_duplicate_counter_error(self, page: Page):
        """Test error when creating duplicate counter names"""
        page.goto(APP_URL)
        
        # Create first counter
        page.fill('[data-testid="counter-name-input"]', "duplicate")
        page.fill('[data-testid="counter-value-input"]', "10")
        page.click('[data-testid="create-counter-btn"]')
        
        expect(page.locator('[data-testid="counter-duplicate"]')).to_be_visible()
        
        # Try to create another counter with the same name
        page.fill('[data-testid="counter-name-input"]', "duplicate")
        page.fill('[data-testid="counter-value-input"]', "20")
        page.click('[data-testid="create-counter-btn"]')
        
        # Check for error toast (Chakra UI toasts appear in a toast container)
        page.wait_for_timeout(500)  # Wait for toast to appear
        expect(page.locator('text=Error')).to_be_visible()

    def test_data_persistence_after_refresh(self, page: Page):
        """Test that counters persist after page refresh"""
        page.goto(APP_URL)
        
        # Create counters
        page.fill('[data-testid="counter-name-input"]', "persistent-1")
        page.fill('[data-testid="counter-value-input"]', "100")
        page.click('[data-testid="create-counter-btn"]')
        
        # Modify counter
        page.click('[data-testid="increment-10-persistent-1"]')
        
        # Refresh the page
        page.reload()
        
        # Check counter is still there with correct value
        expect(page.locator('[data-testid="counter-persistent-1"]')).to_be_visible()
        expect(page.locator('[data-testid="value-persistent-1"]')).to_contain_text("110")

    def test_complex_workflow(self, page: Page):
        """Test a complex workflow with multiple operations"""
        page.goto(APP_URL)
        
        # Create multiple counters
        page.fill('[data-testid="counter-name-input"]', "workflow-1")
        page.fill('[data-testid="counter-value-input"]', "0")
        page.click('[data-testid="create-counter-btn"]')
        
        page.fill('[data-testid="counter-name-input"]', "workflow-2")
        page.fill('[data-testid="counter-value-input"]', "50")
        page.click('[data-testid="create-counter-btn"]')
        
        # Perform various operations
        page.click('[data-testid="increment-10-workflow-1"]')  # 0 -> 10
        page.click('[data-testid="increment-10-workflow-1"]')  # 10 -> 20
        page.click('[data-testid="increment-workflow-1"]')     # 20 -> 21
        
        page.click('[data-testid="decrement-10-workflow-2"]')  # 50 -> 40
        page.click('[data-testid="decrement-workflow-2"]')     # 40 -> 39
        
        # Set direct value for workflow-1
        input_field = page.locator('[data-testid="set-value-workflow-1"]')
        input_field.fill("100")
        input_field.press("Enter")
        
        # Reset workflow-2
        page.click('[data-testid="reset-workflow-2"]')
        
        # Verify final states
        expect(page.locator('[data-testid="value-workflow-1"]')).to_contain_text("100")
        expect(page.locator('[data-testid="value-workflow-2"]')).to_contain_text("0")
        
        # Delete workflow-1
        page.click('[data-testid="delete-workflow-1"]')
        expect(page.locator('[data-testid="counter-workflow-1"]')).not_to_be_visible()
        
        # workflow-2 should still exist
        expect(page.locator('[data-testid="counter-workflow-2"]')).to_be_visible()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])