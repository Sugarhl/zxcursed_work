from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, String, select
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from server.config import SCHEMA

from server.models.base import Base


class LabVariant(Base):
    __tablename__ = "lab_var"
    __table_args__ = ({"schema": f"{SCHEMA}"},)

    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer,
                    ForeignKey(f"{SCHEMA}.lab.id", ondelete="CASCADE"),
                    nullable=False)
    variant_number = Column(Integer, nullable=False)
    variant_filename = Column(String)
    file_data = Column(LargeBinary)

    lab = relationship("Lab", back_populates="variants")
    solutions = relationship("LabSolution", back_populates="variant")
