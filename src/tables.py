from sqlalchemy import Column, Integer, String, LargeBinary, \
    Date, ForeignKey, Boolean, Text, Float, UUID

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

base = declarative_base()


class TypeUser(base):
    __tablename__ = "type_user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(32), nullable=False)
    description = Column(String(128), nullable=True)


class User(base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, unique=True, default=uuid4())

    login = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    id_type = Column(Integer, ForeignKey("type_user.id"))
    type = relationship("TypeUser", lazy="joined")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, val):
        self.hashed_password = generate_password_hash(val)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class TypePoint(base):
    __tablename__ = "type_point"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(32), nullable=False)
    notation = Column(String(4), nullable=False)
    type_data = Column(String(10), nullable=False)
    description = Column(String(128), nullable=True)


class Point(base):
    __tablename__ = "point"
    id = Column(Integer, autoincrement=True, primary_key=True)
    id_user = Column(ForeignKey("user.id"))
    id_type_point = Column(ForeignKey("type_point.id"))
    value = Column(String, nullable=False, default="0.0")
    default_value = Column(String, nullable=True, default="0.0")
    datareg = Column(Date, nullable=True, default=datetime.now())
    type_point = relationship("TypePoint", lazy="joined")

