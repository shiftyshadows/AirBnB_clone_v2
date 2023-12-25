#!/usr/bin/python3
"""Initializes the package"""
from os import environ

HBNB_TYPE_STORAGE = environ.get('HBNB_TYPE_STORAGE')

if HBNB_TYPE_STORAGE == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
