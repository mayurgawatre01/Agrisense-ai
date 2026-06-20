"""
CropSense v2.0 — Flask extensions (db, bcrypt)
Separated to avoid circular imports.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
