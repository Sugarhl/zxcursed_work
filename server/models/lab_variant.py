from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.orm import relationship
from server.config import SCHEMA

from server.models.base import Base


class LabVariant(Base):
    __tablename__ = "lab_var"
    __table_args__ = ({"schema": f"{SCHEMA}"},)

    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(
        Integer, ForeignKey(f"{SCHEMA}.lab.id", ondelete="CASCADE"), nullable=False
    )

    student_id = Column(
        Integer,
        ForeignKey(f"{SCHEMA}.student.id", ondelete="NO ACTION"),
        nullable=False,
    )

    tutor_for_check_id = Column(
        Integer, ForeignKey(f"{SCHEMA}.tutor.id", ondelete="NO ACTION"), nullable=True
    )

    variant_number = Column(Integer, nullable=False)
    variant_filename = Column(String)
    file_key = Column(String)

    student = relationship("Student", back_populates="variants")
    tutor = relationship("Tutor", back_populates="variants_for_check")
    lab = relationship("Lab", back_populates="variants")
    solutions = relationship("LabSolution", back_populates="variant")
