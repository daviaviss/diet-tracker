from sqlalchemy import Column, Enum, Float, Integer, String
from sqlalchemy.orm import relationship

from mvc.models.base import Base
from mvc.models.nutritional_goal import NutritionalGoal


# Representa a tabela "users" no banco de dados SQLite
class User(Base):
    __tablename__ = "users"

    # Chave primária gerada automaticamente pelo banco
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Dados de identificação — e-mail é único e usado como login
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)

    # Senha armazenada como hash bcrypt, nunca em texto puro
    password = Column(String(255), nullable=False)

    # Dados físicos usados para calcular a TMB (Taxa Metabólica Basal)
    age = Column(Integer)
    height = Column(Float)   # em centímetros
    weight = Column(Float)   # em quilogramas
    activity_factor = Column(Float)  # multiplicador da TMB (1.2 a 1.9)

    # Objetivo nutricional do usuário (perder, manter ou ganhar peso)
    goal = Column(Enum(NutritionalGoal))

    # Relacionamentos com outras tabelas — cascade garante que os dados
    # dependentes sejam removidos junto quando o usuário for deletado
    reminders = relationship("Reminder", back_populates="user", cascade="all, delete-orphan")
    physical_activities = relationship("PhysicalActivity", back_populates="user", cascade="all, delete-orphan")
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")
    progress_report = relationship("ProgressReport", back_populates="user", uselist=False, cascade="all, delete-orphan")

    # Define como o objeto aparece no terminal ao fazer print() ou ao depurar
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', goal={self.goal})>"
