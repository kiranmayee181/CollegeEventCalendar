from datetime import datetime
from markdown import markdown
from flask import current_app, request, url_for
from app import db
from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    eid = Column(Integer, autoincrement=True, primary_key=True)
    ename = Column(String(512),nullable=False)
    edesc = Column(String(512),nullable=False)
    edate= Column(String(512),nullable=False)
    edept = Column(String(512),nullable=False)
    evenue = Column(String(512),nullable=False)
    eposter= Column(String(512),nullable=False)
    oname= Column(String(512),nullable=False)
    odept= Column(String(512),nullable=False)
    verified = Column(Integer,default=0)
    ophno = Column(Integer,default=9957685478)

class Organizers(Base):
    __tablename__ = "Organizers"
    ouname = Column(String(512),nullable=False,primary_key=True)
    opwd = Column(String(512),nullable=False)
