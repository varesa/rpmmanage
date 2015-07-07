from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

class Db:
    def __init__(self):
        self.engine = create_engine(
            'sqlite:///:memory:', convert_unicode=True,
            pool_recycle=3600, pool_size=10)
        self.sessionmaker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return scoped_session(self.sessionmaker)

    def get_engine(self):
        return self.engine
