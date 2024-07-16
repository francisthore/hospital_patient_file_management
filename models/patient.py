#!/usr/bin/python3
"""This module represents the patient object"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship


class Patient(BaseModel, Base):
    """Patient object definition"""
    __tablename__ = 'patients'
    fullname = Column(String(100), nullable=False)
    id_number = Column(String(13), nullable=False)
    dob = Column(DateTime, nullable=False)
    sex = Column(String(6), nullable=False)
    address = Column(String(256), nullable=False)
    email = Column(String(100), nullable=True)
    cell = Column(String(10), nullable=True)
    medical_records = relationship('MedicalRecord', backref='patient',
                                   cascade='all, delete, delete-orphan')
    appointments = relationship('Appointment', backref='patient',
                                cascade='all, delete, delete-orphan')
