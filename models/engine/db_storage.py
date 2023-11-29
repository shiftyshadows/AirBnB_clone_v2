#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import environ


class DBStorage:
    """DBStorage class for managing the MySQL database"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage"""
        user = environ.get('HBNB_MYSQL_USER')
        password = environ.get('HBNB_MYSQL_PWD')
        host = environ.get('HBNB_MYSQL_HOST', 'localhost')
        database = environ.get('HBNB_MYSQL_DB')
        env = environ.get('HBNB_ENV')

        connection_str = 'mysql+mysqldb://{}:{}@{}/{}'
        self.__engine = create_engine(
            connection_str.format(user, password, host, database),
            pool_pre_ping=True
        )

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        from models import classes

        objects = {}
        if cls:
            query_result = self.__session.query(classes[cls]).all()
        else:
            query_result = []
            for cls in classes.values():
                query_result.extend(self.__session.query(cls).all())

        for obj in query_result:
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            objects[key] = obj

        return objects

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create the current database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
