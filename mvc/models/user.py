from sqlalchemy import Column, Enum, Float, Integer, String
from sqlalchemy.orm import relationship

from mvc.models.base import Base
from mvc.models.enums import NutritionalGoal


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)
    activity_factor = Column(Float)
    goal = Column(Enum(NutritionalGoal))

    reminders = relationship("Reminder", back_populates="user", cascade="all, delete-orphan")
    physical_activities = relationship("PhysicalActivity", back_populates="user", cascade="all, delete-orphan")
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")
    progress_report = relationship("ProgressReport", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', goal={self.goal})>"
