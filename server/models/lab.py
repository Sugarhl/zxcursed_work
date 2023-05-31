from sqlalchemy import Column, Enum, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from server.config import SCHEMA
from server.generation.generators.base import GenType


from server.models.base import Base


class Lab(Base):
    __tablename__ = "lab"
    __table_args__ = ({"schema": f"{SCHEMA}"},)

    id = Column(Integer, primary_key=True, index=True)
    lab_name = Column(String(255), nullable=False)
    tutor_id = Column(
        Integer, ForeignKey(f"{SCHEMA}.tutor.id", ondelete="NO ACTION"), nullable=False
    )
    date_start = Column(DateTime, nullable=True)
    deadline = Column(DateTime, nullable=True)
    description = Column(String)
    generator_type = Column(Enum(GenType), nullable=False, index=True)
    group_id = Column(
        Integer, ForeignKey(f"{SCHEMA}.group.id", ondelete="CASCADE"), nullable=True
    )

    tutor = relationship("Tutor", back_populates="labs")
    variants = relationship("LabVariant", back_populates="lab")

    group = relationship("Group", back_populates="labs")
