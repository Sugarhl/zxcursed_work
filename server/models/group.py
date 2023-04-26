# from sqlalchemy import Column, Integer, String

# from server.database import SCHEMA

# from sqlalchemy.orm import relationship

# class Group(Base):
#     __tablename__ = "group"
#     __table_args__ = ({"schema": f"{SCHEMA}"},)

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), nullable=False)

#     # Adding the One-to-Many relationship with Student
#     students = relationship("Student", back_populates="group")
