from peewee import *

# Database setup
db = SqliteDatabase('counter.db')

class Counter(Model):
    id = AutoField()
    name = CharField(unique=True)
    value = IntegerField(default=0)

    class Meta:
        database = db
