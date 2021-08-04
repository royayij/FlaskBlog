from sqlalchemy import Column, Integer, String, Text
from app import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer(), primary_key=True)
    description = Column(String(256), nullable=True, unique=False)
    name = Column(String(128), nullable=False, unique=True)
    slug = Column(String(128), nullable=False, unique=True)


class Post(db.Model):
    __tablename__ = 'posts'
    id = Column(Integer(), primary_key=True)
    summary = Column(String(256), nullable=True, unique=False)
    title = Column(String(128), nullable=False, unique=True)
    content = Column(Text(), nullable=False, unique=False)
    slug = Column(String(128), nullable=False, unique=True)
