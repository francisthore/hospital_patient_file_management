#!/usr/bin/python3
"""Models init"""
from models.engine.db_storage import DBStorage

storage = DBStorage()
storage.reload()
