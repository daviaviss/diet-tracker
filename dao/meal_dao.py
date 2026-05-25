from datetime import date as date_type, time as time_type

from mvc.models import Meal
from mvc.models.diet_status import DietStatus
from mvc.models.meal_category import MealCategory
from dao import use_session


# Cria uma nova refeição no banco para o usuário informado
def create_meal(
    user_id: int,
    name: str,
    category: MealCategory,
    status: DietStatus,
    date: date_type,
    time: time_type,
    calories: float,
    protein: float,
    carbs: float,
    fat: float,
) -> Meal:
    with use_session(commit=True) as session:
        meal = Meal(
            user_id=user_id,
            name=name,
            category=category,
            status=status,
            date=date,
            time=time,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
        )
        session.add(meal)
        # flush envia o INSERT antes do commit para que o id seja gerado
        session.flush()
        # refresh carrega os dados do banco de volta para o objeto (ex: id gerado)
        session.refresh(meal)
        return meal


# Retorna todas as refeições de um usuário em uma data específica
def get_meals_by_user_and_date(user_id: int, date: date_type) -> list[Meal]:
    with use_session() as session:
        return (
            session.query(Meal)
            .filter_by(user_id=user_id, date=date)
            .all()
        )


# Busca uma refeição pelo usuário, data e categoria — usado para validar RN001
# (não é permitido cadastrar duas refeições da mesma categoria no mesmo dia)
def get_meal_by_user_date_category(
    user_id: int, date: date_type, category: MealCategory
) -> Meal | None:
    with use_session() as session:
        return (
            session.query(Meal)
            .filter_by(user_id=user_id, date=date, category=category)
            .first()
        )


# Atualiza os campos de uma refeição existente pelo id
def update_meal(meal_id: int, **kwargs) -> Meal | None:
    with use_session(commit=True) as session:
        meal = session.get(Meal, meal_id)
        if meal is None:
            return None
        for key, value in kwargs.items():
            setattr(meal, key, value)
        session.flush()
        session.refresh(meal)
        return meal


# Remove uma refeição pelo id — retorna False se não existir
def delete_meal(meal_id: int) -> bool:
    with use_session(commit=True) as session:
        meal = session.get(Meal, meal_id)
        if meal is None:
            return False
        session.delete(meal)
        return True


# Soma as calorias de todas as refeições de um usuário em uma data
def get_total_calories(user_id: int, date: date_type) -> float:
    with use_session() as session:
        meals = (
            session.query(Meal)
            .filter_by(user_id=user_id, date=date)
            .all()
        )
        return sum(m.calories or 0 for m in meals)
