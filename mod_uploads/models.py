from app import db
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


class File(db.Model):
    __tablename__ = 'files'
    id = Column(Integer(), primary_key=True)
    filename = Column(String(256), nullable=False, unique=True)
    upload_date = Column(DateTime(), nullable=False, unique=False, default=datetime.utcnow)
