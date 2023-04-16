from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from server.database import Base


class Lab(Base):
    __tablename__ = "lab"
    id = Column(Integer, primary_key=True, index=True)
    lab_name = Column(String(255), nullable=False)
    description = Column(String)
    owner = Column(String(255), nullable=False)
    file_of_lab = Column(String)

    variants = relationship("LabVariant", back_populates="lab")


class Tutor(Base):
    __tablename__ = "tutor"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)

    solutions = relationship("LabSolution", back_populates="tutor")


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)

    solutions = relationship("LabSolution", back_populates="student")
    results = relationship("LabResult", back_populates="student")


class User(Base):
    __tablename__ = "login_creds"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    user_type = Column(String(50), nullable=False, index=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    CheckConstraint("user_type IN ('Student', 'Tutor')")


class LabVariant(Base):
    __tablename__ = "lab_var"
    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey(
        "lab.id", ondelete="CASCADE"), nullable=False)
    variant_name = Column(String(255), nullable=False)
    description = Column(String)

    lab = relationship("Lab", back_populates="variants")
    solutions = relationship("LabSolution", back_populates="variant")


class LabSolution(Base):
    __tablename__ = "lab_solution"
    id = Column(Integer, primary_key=True, index=True)
    lab_variant_id = Column(Integer, ForeignKey(
        "lab_var.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey(
        "student.id", ondelete="CASCADE"), nullable=False)
    tutor_id = Column(Integer, ForeignKey(
        "tutor.id", ondelete="CASCADE"), nullable=False)
    solution_filename = Column(String)
    file_data = Column(LargeBinary)
    mark = Column(Integer)

    variant = relationship("LabVariant", back_populates="solutions")
    student = relationship("Student", back_populates="solutions")
    tutor = relationship("Tutor", back_populates="solutions")
    comments = relationship("LabSolutionComment", back_populates="solution")


class LabSolutionComment(Base):
    __tablename__ = "lab_solution_comment"
    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(Integer, ForeignKey(
        "lab_solution.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey(
        "login_creds.id", ondelete="CASCADE"), nullable=False)
    user_type = Column(String(50), nullable=False, index=True)
    reply_id = Column(Integer, nullable=True)
    comment_text = Column(String)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)

    solution = relationship("LabSolution", back_populates="comments")


class LabResult(Base):
    __tablename__ = "lab_result"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey(
        "student.id", ondelete="CASCADE"), nullable=False)
    lab_variant_id = Column(Integer, ForeignKey(
        "lab_var.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer)
    submission_date = Column(DateTime)

    student = relationship("Student", back_populates="results")
