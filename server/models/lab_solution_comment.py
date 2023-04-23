from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from server.config import SCHEMA

from server.models.base import Base


class LabSolutionComment(Base):
    __tablename__ = "lab_solution_comment"
    __table_args__ = ({"schema": f"{SCHEMA}"},)

    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(Integer, ForeignKey(
        f"{SCHEMA}.lab_solution.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    user_type = Column(String(50), nullable=False, index=True)
    reply_id = Column(Integer, nullable=True)
    comment_text = Column(String)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)

    solution = relationship("LabSolution", back_populates="comments")
