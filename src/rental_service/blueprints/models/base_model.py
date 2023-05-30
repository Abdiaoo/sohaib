import os
from peewee import Model, SqliteDatabase

db_path = os.path.join(os.getcwd(), 'database.db')

sqlite_db = SqliteDatabase(db_path)

class BaseModel(Model):
    class Meta:
        database = sqlite_db
