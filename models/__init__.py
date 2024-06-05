#!/usr/bin/python3
"""Initializes the package"""
from os import environ
#from models.state import State
#from models.base_model import BaseModel

#environ["HBNB_MYSQL_USER"] = "hbnb_dev"
#environ["HBNB_MYSQL_PWD"] = "hbnb_dev_pwd"
#environ["HBNB_MYSQL_HOST"] = "localhost"
#environ["HBNB_MYSQL_DB"] = "hbnb_dev_db"
#environ["HBNB_TYPE_STORAGE"] = "db"
#environ["HBNB_ENV"] = "test1"

HBNB_TYPE_STORAGE = environ.get('HBNB_TYPE_STORAGE')

if HBNB_TYPE_STORAGE == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

try:
    storage.reload()
except Exception as e:
    print("Error on storage.reload:", e)
