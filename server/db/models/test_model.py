from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Numeric

from server.db.common import Base


class TestModel(Base):  # type: ignore
    __tablename__ = 'test_table'

    id: int = Column(Integer, primary_key=True)
    uid: str = Column(String, unique=True)
    name: str = Column(String)


class TestData(BaseModel):
    uid: str
    name: str
