from peewee import *
from config.environment import DATABASE_PATH

# Database setup
db = SqliteDatabase(DATABASE_PATH)

class Todo(Model):
    id = AutoField()
    title = CharField()
    description = TextField(default='')
    completed = BooleanField(default=False)

    class Meta:
        database = db
