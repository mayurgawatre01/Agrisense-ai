"""
CropSense v2.0 — Database Models
"""
from extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(150), unique=True, nullable=False)
    phone      = db.Column(db.String(15))
    password   = db.Column(db.String(200), nullable=False)
    role       = db.Column(db.String(10), default='farmer')
    state      = db.Column(db.String(50))
    district   = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    crops       = db.relationship('CropData', backref='user', lazy=True)
    predictions = db.relationship('Prediction', backref='user', lazy=True)


class CropData(db.Model):
    __tablename__ = 'crop_data'

    id                = db.Column(db.Integer, primary_key=True)
    user_id           = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    state             = db.Column(db.String(50))
    district          = db.Column(db.String(50))
    crop_year         = db.Column(db.Integer)
    season            = db.Column(db.String(20))
    crop              = db.Column(db.String(50))
    area              = db.Column(db.Float)
    production        = db.Column(db.Float)
    yield_per_hectare = db.Column(db.Float)
    uploaded_at       = db.Column(db.DateTime, default=datetime.utcnow)


class Prediction(db.Model):
    __tablename__ = 'predictions'

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    state            = db.Column(db.String(50))
    district         = db.Column(db.String(50))
    season           = db.Column(db.String(20))
    crop             = db.Column(db.String(50))
    area             = db.Column(db.Float)
    predicted_yield  = db.Column(db.Float)
    confidence       = db.Column(db.Float)
    total_production = db.Column(db.Float)
    model_used       = db.Column(db.String(100))
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)
