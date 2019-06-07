from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db import Base


class Rack(Base):
    __tablename__ = 'rack'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, server_default=func.now(), nullable=False)
    changed = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    size = Column(Integer, default=0, nullable=False)
    capacity = Column(Integer, nullable=False)
    servers = relationship('Server', back_populates='rack')

    def __init__(self, capacity, size=None, created=None, changed=None, id=None):
        self.id = id
        self.created = created
        self.changed = changed
        self.size = size
        self.capacity = capacity

    def __repr__(self):
        return f'Rack: id: {self.id}, size: {self.size}, capacity: {self.capacity}'


class Server(Base):
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, server_default=func.now(), nullable=False)
    changed = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    rack_id = Column(Integer, ForeignKey('rack.id'), nullable=False)
    rack = relationship('Rack', back_populates='servers')

    def __init__(self, rack_id, created=None, changed=None, id=None):
        self.id = id
        self.created = created
        self.changed = changed
        self.rack_id = rack_id

    def __repr__(self):
        return f'Server: id: {self.id}, rack id: {self.rack_id}'
