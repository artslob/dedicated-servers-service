from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func

from .db import Base


class Rack(Base):
    __tablename__ = 'rack'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, server_default=func.now(), nullable=False)
    changed = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    size = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)

    def __init__(self, size, capacity, created=None, changed=None, id=True):
        self.id = id
        self.created = created
        self.changed = changed
        self.size = size
        self.capacity = capacity

    def __repr__(self):
        return f'Rack: id: {self.id}, size: {self.size}, capacity: {self.capacity}'
