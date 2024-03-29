import enum

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum as alchemyEnum, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db import Base


class ToDictMixin:
    def as_dict(self):
        if hasattr(self, '_to_dict_mixin_columns'):
            columns = self._to_dict_mixin_columns
        else:
            columns = self.__table__.columns.keys()
        result = {}
        for name in columns:
            attr = getattr(self, name)
            if isinstance(attr, enum.Enum):
                attr = attr.name
            result[name] = attr
        return result


class RackCapacities(enum.Enum):
    ten = 10
    twenty = 20


class Rack(Base, ToDictMixin):
    __tablename__ = 'rack'
    __table_args__ = (
        CheckConstraint('size <= capacity_int'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, server_default=func.now(), nullable=False)
    changed = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    size = Column(Integer, default=0, nullable=False)
    capacity_int = Column(Integer, nullable=False)
    capacity = Column(alchemyEnum(RackCapacities), nullable=False)
    servers = relationship('Server', back_populates='rack')

    _to_dict_mixin_columns = ('id', 'created', 'changed', 'size', 'capacity', 'capacity_int')

    def __init__(self, capacity: RackCapacities, size=None, created=None, changed=None, id=None):
        self.id = id
        self.created = created
        self.changed = changed
        self.size = size
        self.capacity = capacity
        self.capacity_int = capacity.value

    def __repr__(self):
        return f'Rack: id: {self.id}, size: {self.size}, capacity: {self.capacity}'

    def increase_size(self):
        self.size = Rack.size + 1

    def decrease_size(self):
        self.size = Rack.size - 1


class ServerStatuses(enum.Enum):
    unpaid = enum.auto()
    paid = enum.auto()
    active = enum.auto()
    deleted = enum.auto()

    @classmethod
    def status_names(cls):
        return [e.name for e in cls]


class Server(Base, ToDictMixin):
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, server_default=func.now(), nullable=False)
    changed = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    status = Column(alchemyEnum(ServerStatuses), default=ServerStatuses.unpaid, nullable=False)
    rack_id = Column(Integer, ForeignKey('rack.id'), nullable=True)
    rack = relationship('Rack', back_populates='servers')

    _to_dict_mixin_columns = ('id', 'created', 'changed', 'rack_id', 'status')

    def __init__(self, rack_id, created=None, changed=None, id=None, status=None):
        self.id = id
        self.created = created
        self.changed = changed
        self.status = status
        self.rack_id = rack_id

    def __repr__(self):
        return f'Server: id: {self.id}, rack id: {self.rack_id}'

    @classmethod
    def from_json(cls, content):
        if not content or not isinstance(content, dict):
            return None

        columns = ('rack_id',)
        if any(c not in content for c in columns):
            return None

        return Server(**{c: content[c] for c in columns})
