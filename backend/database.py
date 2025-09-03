import os
import tempfile
from peewee import SqliteDatabase

# Database setup - environment-aware
def get_db():
    app_env = os.getenv("APP_ENV", "development")
    if app_env == "test":
        test_db_file = os.path.join(tempfile.gettempdir(), "todos_test.sqlite")
        return SqliteDatabase(test_db_file)
    else:
        return SqliteDatabase("todos_development.sqlite")

db = get_db()