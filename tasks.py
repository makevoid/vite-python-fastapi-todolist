"""
Invoke tasks for the full-stack todo list application.
Run with: inv <task-name>
"""

from invoke import task
import os


@task
def backend(ctx):
    """Run the FastAPI backend development server"""
    with ctx.cd("backend"):
        ctx.run("uvicorn main:app --reload --host 0.0.0.0 --port 8000")


@task
def frontend(ctx):
    """Run the React frontend development server"""
    with ctx.cd("frontend"):
        ctx.run("npm run dev")


@task
def test_api(ctx):
    """Run backend API tests"""
    with ctx.cd("backend"):
        ctx.run("python3 -m pytest test_api.py -v")


@task
def test_e2e(ctx):
    """Run end-to-end tests"""
    with ctx.cd("e2e"):
        ctx.run("python3 -m pytest test_todo_e2e.py -v")


@task
def test_all(ctx):
    """Run all tests (API + E2E)"""
    print("Running backend API tests...")
    test_api(ctx)
    print("\nRunning E2E tests...")
    test_e2e(ctx)


@task
def install_backend(ctx):
    """Install backend dependencies"""
    with ctx.cd("backend"):
        ctx.run("pip install -r requirements.txt")


@task
def install_frontend(ctx):
    """Install frontend dependencies"""
    with ctx.cd("frontend"):
        ctx.run("npm install")


@task
def install(ctx):
    """Install all dependencies (backend + frontend)"""
    install_backend(ctx)
    install_frontend(ctx)


@task
def build_frontend(ctx):
    """Build frontend for production"""
    with ctx.cd("frontend"):
        ctx.run("npm run build")


@task
def preview_frontend(ctx):
    """Preview production build of frontend"""
    with ctx.cd("frontend"):
        ctx.run("npm run preview")


@task
def docker_up(ctx):
    """Start all services with Docker Compose"""
    ctx.run("docker-compose up --build")


@task
def docker_down(ctx):
    """Stop all Docker Compose services"""
    ctx.run("docker-compose down")


@task
def clean(ctx):
    """Clean build artifacts and cache"""
    print("Cleaning backend...")
    with ctx.cd("backend"):
        ctx.run("rm -f todo.db", warn=True)
        ctx.run("rm -rf __pycache__", warn=True)
        ctx.run("rm -rf .pytest_cache", warn=True)
    
    print("Cleaning frontend...")
    with ctx.cd("frontend"):
        ctx.run("rm -rf dist", warn=True)
        ctx.run("rm -rf node_modules/.cache", warn=True)
    
    print("Cleaning e2e...")
    with ctx.cd("e2e"):
        ctx.run("rm -rf __pycache__", warn=True)
        ctx.run("rm -rf .pytest_cache", warn=True)


@task
def dev(ctx):
    """Show development server startup commands"""
    print("To run the full development environment:")
    print("1. Backend:  inv backend")
    print("2. Frontend: inv frontend")
    print("3. Or run both in separate terminals")
    print("\nAPI docs available at: http://localhost:8000/docs")
    print("Frontend available at: http://localhost:5173")