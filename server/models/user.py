from sqlalchemy import Column, Integer, String
# from sqlalchemy.dialects.postgresql import UUID  MAYBE LATER
from server.config import SCHEMA
from sqlalchemy import Enum

from server.models.base import Base
from server.utils import UserType


class User(Base):
    __tablename__ = "login_creds"
    __table_args__ = ({"schema": f"{SCHEMA}"},)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    user_type = Column(Enum(UserType), nullable=False, index=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
