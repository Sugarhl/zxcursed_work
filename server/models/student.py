from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from server.config import SCHEMA


from server.models.base import Base


class Student(Base):
    __tablename__ = "student"
    __table_args__ = ({"schema": f"{SCHEMA}"},)

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    group_id = Column(
        Integer, ForeignKey(f"{SCHEMA}.group.id", ondelete="NO ACTION"), nullable=True
    )

    variants = relationship("LabVariant", back_populates="student")
