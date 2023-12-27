#!/usr/bin/python3
""" This module defines the User class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, create_engine


class User(BaseModel, Base):
    """ User class that inherits from BaseModel """
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

engine = create_engine(
    "mysql+mysqldb://hbnb_dev:hbnb_dev_pwd@localhost/hbnb_dev_db", echo=False)
Base.metadata.create_all(engine)
