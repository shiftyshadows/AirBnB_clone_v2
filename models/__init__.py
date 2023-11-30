#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import environ
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

storage_type = environ.get('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
