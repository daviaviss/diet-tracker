from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from mvc.models.base import Base


class PhysicalActivity(Base):
    __tablename__ = "physical_activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    calories_burned = Column(Float)
    duration = Column(Integer)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="physical_activities")

    def __repr__(self):
        return f"<PhysicalActivity(id={self.id}, name='{self.name}', calories_burned={self.calories_burned})>"
