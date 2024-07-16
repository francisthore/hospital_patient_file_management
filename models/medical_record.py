#!/usr/bin/python3
"""This module represents the medical record
object of a patient"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class MedicalRecord(BaseModel, Base):
    """Definition of the medical records"""
    __tablename__ = 'medical_records'
    patient_id = Column(String(60), ForeignKey('patients.id'), nullable=False)
    staff_id = Column(String(60), ForeignKey('staff.id'), nullable=False)
    diagnosis = Column(String(1024), nullable=False)
    prescription = Column(String(1024), nullable=False)
