#!/usr/bin/python3
"""Staff represents the medical staff be
it receptionist, nurse or doctor"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Staff(BaseModel, Base):
    """Respresentation of the staff"""
    __tablename__ = 'staff'
    fullname = Column(String(100), nullable=False)
    id_number = Column(String(13), nullable=False)
    dob = Column(DateTime, nullable=False)
    sex = Column(String(6), nullable=False)
    address = Column(String(256), nullable=False)
    email = Column(String(100), nullable=False)
    cell = Column(Integer, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), default=None)
    user = relationship("User", backref="staff")
    appointments = relationship('Appointment', backref='staff',
                                cascade='all, delete, delete-orphan')
