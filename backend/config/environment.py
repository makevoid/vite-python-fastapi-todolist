import os
import tempfile

# Environment constants
APP_ENV = os.getenv("APP_ENV", "development")

# Environment types
DEVELOPMENT = "development"
TEST = "test"
PRODUCTION = "production"

# Database paths
DEVELOPMENT_DB_PATH = "todos_development.sqlite"
TEST_DB_PATH = os.path.join(tempfile.gettempdir(), "todos_test.sqlite")
PRODUCTION_DB_PATH = "todos_production.sqlite"

# Server configuration
DEVELOPMENT_HOST = "0.0.0.0"
DEVELOPMENT_PORT = 8000
TEST_HOST = "0.0.0.0"
TEST_PORT = 8001
PRODUCTION_HOST = "0.0.0.0"
PRODUCTION_PORT = 8000

# CORS origins
DEVELOPMENT_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]
TEST_ORIGINS = ["http://localhost:5174"]
PRODUCTION_ORIGINS = []  # Should be configured for production

# Environment-based configuration
if APP_ENV == TEST:
    DATABASE_PATH = TEST_DB_PATH
    SERVER_HOST = TEST_HOST
    SERVER_PORT = TEST_PORT
    CORS_ORIGINS = TEST_ORIGINS
    APP_TITLE = "Todo API - Test"
    RELOAD = False
elif APP_ENV == PRODUCTION:
    DATABASE_PATH = PRODUCTION_DB_PATH
    SERVER_HOST = PRODUCTION_HOST
    SERVER_PORT = PRODUCTION_PORT
    CORS_ORIGINS = PRODUCTION_ORIGINS
    APP_TITLE = "Todo API - Production"
    RELOAD = False
else:  # Default to development
    DATABASE_PATH = DEVELOPMENT_DB_PATH
    SERVER_HOST = DEVELOPMENT_HOST
    SERVER_PORT = DEVELOPMENT_PORT
    CORS_ORIGINS = DEVELOPMENT_ORIGINS
    APP_TITLE = "Todo API"
    RELOAD = True