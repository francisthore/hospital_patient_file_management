#!/usr/bin/python3
"""
    Base Model class for the project
    where all other models will be inheriting from

    Defines the common 3 attributes that all objects will
    have and common methods.
"""
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid
import models

Base = declarative_base()


class BaseModel:
    """The Base Model class which contains common
    attributes and methods for the other models in
    the project
    """
    id = Column(String(60), nullable=False, primary_key=True,
                default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        """Object instantiation either from dictionary
        or from start"""
        if kwargs:
            """Initializing from a dict"""
            for k, v in kwargs.items():
                if k != '__class__':
                    setattr(self, k, v)
            if 'created_at' in kwargs and isinstance(self.created_at, str):
                self.created_at = datetime.strptime(kwargs['created_at'],
                                                    "%Y-%m-%d %H:%M:%S")
            else:
                self.created_at = datetime.now()
            if 'updated_at' in kwargs and isinstance(self.updated_at, str):
                self.updated_at = datetime.strptime(kwargs['updated_at'],
                                                    "%Y-%m-%d %H:%M:%S")
            else:
                self.updated_at = datetime.now()
            if 'id' not in kwargs or kwargs['id'] is None:
                self.id = str(uuid.uuid4())
        else:
            """Initializing from scratch"""
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """String representation of object"""
        return '[{}] ({}) {}'.format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Saves changes to object"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Serilizes object for storage"""
        obj_dict = self.__dict__.copy()
        if 'created_at' in obj_dict:
            obj_dict['created_at'] = obj_dict['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        if 'updated_at' in obj_dict:
            obj_dict['updated_at'] = obj_dict['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
        obj_dict['__class__'] = self.__class__.__name__
        if '_sa_instance_state' in obj_dict:
            del obj_dict['_sa_instance_state']
        return obj_dict

    def delete(self):
        """Deletes current object instance from db"""
        models.storage.delete(self)
