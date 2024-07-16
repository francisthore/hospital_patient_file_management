#!/usr/bin/python3
"""Appointments representation"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey


class Appointment(BaseModel, Base):
    """Defines the appointments of a patient"""
    __tablename__ = 'appointments'
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    staff_id = Column(String(60), ForeignKey('staff.id'), nullable=True)
    date = Column(DateTime, nullable=True)
