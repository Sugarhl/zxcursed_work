from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from server.config import SCHEMA

from server.models.base import Base


class LabSolution(Base):
    __tablename__ = "lab_solution"
    __table_args__ = ({"schema": f"{SCHEMA}"},)

    id = Column(Integer, primary_key=True, index=True)
    lab_variant_id = Column(
        Integer, ForeignKey(f"{SCHEMA}.lab_var.id", ondelete="CASCADE"), nullable=False
    )

    solution_filename = Column(String)
    file_key = Column(String)

    auto_mark = Column(Integer)
    tutor_mark = Column(Integer)

    tutor_comment = Column(String)
    student_comment = Column(String)

    variant = relationship("LabVariant", back_populates="solutions")
    comments = relationship("LabSolutionComment", back_populates="solution")
