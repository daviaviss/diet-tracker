from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from mvc.models.base import Base
from mvc.models.diet_status import DietStatus
from mvc.models.meal_category import MealCategory


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    calories = Column(Float)
    carbs = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    category = Column(Enum(MealCategory))
    status = Column(Enum(DietStatus))
    date = Column(Date, nullable=False)
    time = Column(Time)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="meals")
    progress_reports = relationship("ProgressReport", secondary="progress_report_meals", back_populates="meals")

    def __repr__(self):
        return f"<Meal(id={self.id}, name='{self.name}', category={self.category}, status={self.status})>"
