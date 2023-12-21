from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from ..db import Base


class Dog(Base):
    __tablename__ = "dogs"

    name = Column(String)
    kind = Column(String)
    pk = Column(Integer, primary_key=True, unique=True)


class Timestamp(Base):
    __tablename__ = "timestamps"

    id = Column(Integer, primary_key=True, unique=True)
    timestamp = Column(DateTime, default=datetime.now())
