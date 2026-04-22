from sqlalchemy import Column, Float, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from mvc.models.base import Base

progress_report_meals = Table(
    "progress_report_meals",
    Base.metadata,
    Column("progress_report_id", Integer, ForeignKey("progress_reports.id"), primary_key=True),
    Column("meal_id", Integer, ForeignKey("meals.id"), primary_key=True),
)


class ProgressReport(Base):
    __tablename__ = "progress_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_meals = Column(Integer, default=0)
    meals_on_diet = Column(Integer, default=0)
    meals_off_diet = Column(Integer, default=0)
    percentage_on_diet = Column(Float, default=0.0)
    net_calories = Column(Float, default=0.0)
    weight_change = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="progress_report")
    meals = relationship("Meal", secondary=progress_report_meals, back_populates="progress_reports")

    def __repr__(self):
        return f"<ProgressReport(id={self.id}, total_meals={self.total_meals}, on_diet={self.percentage_on_diet}%)>"
