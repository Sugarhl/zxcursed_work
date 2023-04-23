from sqlalchemy import Column, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from server.config import SCHEMA


from server.models.base import Base


class Lab(Base):
    __tablename__ = "lab"
    __table_args__ = ({"schema": f"{SCHEMA}"},)

    id = Column(Integer, primary_key=True, index=True)
    lab_name = Column(String(255), nullable=False)
    description = Column(String)
    tutor_id = Column(Integer, ForeignKey(f"{SCHEMA}.tutor.id"), nullable=False)
    file_of_lab = Column(String)

    tutor = relationship("Tutor", back_populates="labs")
    variants = relationship("LabVariant", back_populates="lab")
