from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from server.models.base import Base
from server.config import SCHEMA


class Group(Base):
    __tablename__ = "group"
    __table_args__ = ({"schema": f"{SCHEMA}"})

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    tutor_id = Column(Integer, ForeignKey(
        f"{SCHEMA}.tutor.id", ondelete="NO ACTION"), nullable=True)

    tutor = relationship('Tutor', back_populates='groups')
    students = relationship('Student', backref='group')
