from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from server.config import SCHEMA

from server.models.base import Base


class LabSolution(Base):
    __tablename__ = "lab_solution"
    __table_args__ = ({"schema": f"{SCHEMA}"},)

    id = Column(Integer, primary_key=True, index=True)
    lab_variant_id = Column(Integer,
                            ForeignKey(f"{SCHEMA}.lab_var.id", ondelete="CASCADE"),
                            nullable=False)
    student_id = Column(Integer,
                        ForeignKey(f"{SCHEMA}.student.id", ondelete="CASCADE"),
                        nullable=False)
    tutor_id = Column(Integer,
                      ForeignKey(f"{SCHEMA}.tutor.id", ondelete="NO ACTION"),
                      nullable=False)
    solution_filename = Column(String)
    file_data = Column(LargeBinary)
    mark = Column(Integer)

    variant = relationship("LabVariant", back_populates="solutions")
    student = relationship("Student", back_populates="solutions")
    tutor = relationship("Tutor", back_populates="solutions")
    comments = relationship("LabSolutionComment", back_populates="solution")
