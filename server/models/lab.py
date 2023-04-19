from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from server.config import SCHEMA


from server.models.base import BaseRW


class Lab(BaseRW):
    __tablename__ = "lab"
    __table_args__ = ({"schema": f"{SCHEMA}"},)

    id = Column(Integer, primary_key=True, index=True)
    lab_name = Column(String(255), nullable=False)
    description = Column(String)
    owner = Column(String(255), nullable=False)
    file_of_lab = Column(String)

    variants = relationship("LabVariant", back_populates="lab")
