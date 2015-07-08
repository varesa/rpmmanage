from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

base = declarative_base()

class Test(base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    name = Column(String)

project_target_assoc = Table(
    'project_target_assoc', base.metadata,
     Column('project_id', Integer, ForeignKey("projects.id")),
     Column('target_id', Integer, ForeignKey("targets.id"))
)

class Project(base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    git_url = Column(String)
    targets = relationship('Target', backref="projects", secondary=project_target_assoc)

class Target(base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Build(base):
    __tablename__ = "builds"
    id = Column(Integer, primary_key=True)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", backref="builds")
    target_id = Column(Integer, ForeignKey("targets.id"))
    target = relationship("Target", backref="builds")
    version = Column(String)

    #tasks

class Task(base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    output = Column(String)
    status = Column(String)

def create_tables(database):
    base.metadata.create_all(database.get_engine())

    session = database.get_session()
    if len(session.query(Target).all()) < 2:
        session.add(Target(name="t1"))
        session.add(Target(name="t2"))
    session.commit()
    session.close()
    """
    if len(session.query(Project).all()) == 0:
        session.add(Project(name="Project 1", ))
        session.add(Project(name="Project 2"))
    session.commit()
    print(session.query(Project).all())
    session.close()"""
