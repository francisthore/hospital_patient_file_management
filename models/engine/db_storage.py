#!/usr/bin/python3
"""Database Handling Module"""
from models.base_model import Base
from models.patient import Patient
from models.appointments import Appointment
from models.medical_record import MedicalRecord
from models.user import User
from models.staff import Staff
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

load_dotenv()
DB_U = os.getenv('DB_USERNAME')
DB_P = os.getenv('DB_PASSWORD')
DB_H = os.getenv('DB_HOST')
DB_N = os.getenv('DB_NAME')



classes = {
    'Patient': Patient, 'Appointment': Appointment,
    'MedicalRecord': MedicalRecord, 'Staff': Staff, 'User': User
}


class DBStorage():
    """Storange handling class"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate storage object and creates engine and
        session"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(DB_U,
                                                        DB_P, DB_H, DB_N),
                                      pool_pre_ping=True)

    def reload(self):
        """Creates all tables in db and a current db session"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def get(self, cls, id):
        """Fetches one object from the db"""
        if type(cls) is str and cls in classes:
            cls = classes[cls]
            return self.__session.query(cls).filter(cls.id == id).first()
        elif type(cls) is not None:
            return self.__session.query(cls).filter(cls.id == id).first()
        else:
            return None
        
    def get_by_user_id(self, cls, id):
        """Fetches one object from the db by user_id"""
        if type(cls) is str and cls in classes:
            cls = classes[cls]
            return self.__session.query(cls).filter(cls.user_id == id).first()
        elif type(cls) is not None:
            return self.__session.query(cls).filter(cls.user_id == id).first()
        else:
            return None
        
    def get_id_by_user_id(self, cls, id):
        """Fetches one object from the db by user_id"""
        if type(cls) is str and cls in classes:
            cls = classes[cls]
            return self.__session.query(cls).filter(cls.user_id == id).first().id
        elif type(cls) is not None:
            return self.__session.query(cls).filter(cls.user_id == id).first().id
        else:
            return None
        
    def get_by_id_number(self, cls, id):
        """Fetches one object from the db by id_number"""
        if type(cls) is str and cls in classes:
            cls = classes[cls]
            return self.__session.query(cls).filter(cls.id_number == id).first()
        elif type(cls) is not None:
            return self.__session.query(cls).filter(cls.id_number == id).first()
        else:
            return None

    def new(self, obj):
        """Adds object to the db"""
        self.__session.add(obj)

    def save(self):
        """Commits changes to db"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the db"""
        if obj is not None:
            self.__session.delete(obj)

    def all(self, cls=None):
        """Makes a db query for objects and returns
        a dictionary of the objects"""
        objects_dict = {}
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            if cls:
                objects = self.__session.query(cls).all()
                for obj in objects:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects_dict[key] = obj
        else:
            for klas in classes.values():
                objects = self.__session.query(klas).all()
                for obj in objects:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects_dict[key] = obj
        return objects_dict

    def close(self):
        """Closes db session"""
        self.__session.close()

    def count(self, cls=None):
        """Counts objects belonging to the passed
        class or all objects in db if no class is passed"""
        if cls is None:
            return len(self.all())
        if isinstance(cls, str):
            cls = classes.get(cls)
            return len(self.all(cls))
        else:
            return len(self.all(cls))
        
    
    def check_email(self, email):
        """Checks if an email is in the db"""
        user = self.__session.query(User).filter(User.email == email).first()
        if user:
            return True
        return None
    
    def check_username(self, username):
        user = self.__session.query(User).filter(User.username == username).first()
        if user:
            return True
        return False

    def get_user(self, username):
        """Retrieves a user by username"""
        user = self.__session.query(User).filter(User.username == username).first()
        if user:
            return user
        return None
    
    def get_user_by_verification_token(self, token):
        """Fetches a user by verification token"""
        return self.__session.query(User).filter(User.verification_token == token).first()
