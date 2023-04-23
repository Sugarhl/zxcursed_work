from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from server.config import SCHEMA

from server.models.base import Base


class Tutor(Base):
    __tablename__ = "tutor"
    __table_args__ = ({"schema": f"{SCHEMA}"},)

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)

    labs = relationship("Lab", back_populates="tutor")
    solutions = relationship("LabSolution", back_populates="tutor")