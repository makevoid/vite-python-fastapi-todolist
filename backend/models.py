from peewee import *

# Database setup
db = SqliteDatabase('todo.db')

class Todo(Model):
    id = AutoField()
    title = CharField()
    description = TextField(default='')
    completed = BooleanField(default=False)

    class Meta:
        database = db
