from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Zone(Base):
    __tablename__ = 'zone'

    name = Column(String, primary_key=True)
    ip = Column(String)
    port = Column(Integer)

    def __repr__(self):
        return f"{self.name} --- {self.ip} --- {self.port}"


from sqlalchemy import create_engine
import os

db_path = os.path.dirname(__file__) + '/database.sqlite'

engine = create_engine(f'sqlite:///{db_path}', echo=True)