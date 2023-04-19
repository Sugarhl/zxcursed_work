from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from server.config import SCHEMA

from server.models.base import BaseRW


class LabResult(BaseRW):
    __tablename__ = "lab_result"
    __table_args__ = ({"schema": f"{SCHEMA}"},)

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey(
        f"{SCHEMA}.student.id", ondelete="CASCADE"), nullable=False)
    lab_variant_id = Column(Integer, ForeignKey(
        f"{SCHEMA}.lab_var.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer)
    submission_date = Column(DateTime)

    student = relationship("Student", back_populates="results")
