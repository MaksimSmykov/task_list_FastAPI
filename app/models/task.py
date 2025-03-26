from sqlalchemy import Column, Integer, String, Boolean, Time, Date
from app.backend.db import Base

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    priority = Column(String)
    completed = Column(Boolean, default=False)
    add_info = Column(String, index=True, nullable=True)
    time = Column(String, nullable=True)
    date = Column(String, nullable=True)

from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))