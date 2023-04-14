from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from server.database import Base


class Lab(Base):
    __tablename__ = "lab"
    id = Column(Integer, primary_key=True, index=True)
    lab_name = Column(String(255), nullable=False)
    description = Column(String)
    owner = Column(String(255), nullable=False)
    file_of_lab = Column(String)


class Tutor(Base):
    __tablename__ = "tutor"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)


class User(Base):
    __tablename__ = "login_creds"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    user_type = Column(String(50), nullable=False, index=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    CheckConstraint("user_type IN ('Student', 'Tutor')")


class LabVariant(Base):
    __tablename__ = "lab_var"
    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey(
        "lab.id", ondelete="CASCADE"), nullable=False)
    variant_name = Column(String(255), nullable=False)
    description = Column(String)
    lab = relationship("Lab", back_populates="variants")


Lab.variants = relationship(
    "LabVariant", order_by=LabVariant.id, back_populates="lab")


class LabSolution(Base):
    __tablename__ = "lab_solution"
    id = Column(Integer, primary_key=True, index=True)
    lab_variant_id = Column(Integer, ForeignKey(
        "lab_var.id", ondelete="CASCADE"), nullable=False)
    solution_text = Column(String)
    lab_variant = relationship("LabVariant", back_populates="solutions")


LabVariant.solutions = relationship(
    "LabSolution", order_by=LabSolution.id, back_populates="lab_variant")


class LabResult(Base):
    __tablename__ = "lab_result"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey(
        "student.id", ondelete="CASCADE"), nullable=False)
    lab_variant_id = Column(Integer, ForeignKey(
        "lab_var.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer)
    submission_date = Column(DateTime)
    student = relationship("Student", back_populates="lab_results")
    lab_variant = relationship("LabVariant", back_populates="lab_results")


Student.lab_results = relationship(
    "LabResult",  cascade="save-update, merge, delete, delete-orphan", order_by=LabResult.id, back_populates="student")
LabVariant.lab_results = relationship(
    "LabResult", order_by=LabResult.id, back_populates="lab_variant")
