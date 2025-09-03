from peewee import SqliteDatabase
from config.environment import DATABASE_PATH

# Database setup - environment-aware
def get_db():
    return SqliteDatabase(DATABASE_PATH)

db = get_db()