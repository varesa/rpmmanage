from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, Integer

base = declarative_base()

class Test(base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Project(base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    name = Column(String)

def create_tables(engine):
    base.metadata.create_all(engine)