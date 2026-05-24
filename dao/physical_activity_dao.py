from datetime import date as date_type

from mvc.models import PhysicalActivity
from dao import use_session


# Cria uma nova atividade física no banco para o usuário informado
def create_activity(
    user_id: int, name: str, date: date_type, duration: int, calories_burned: float
) -> PhysicalActivity:
    with use_session(commit=True) as session:
        activity = PhysicalActivity(
            user_id=user_id,
            name=name,
            date=date,
            duration=duration,
            calories_burned=calories_burned,
        )
        session.add(activity)
        session.flush()
        session.refresh(activity)
        return activity


# Retorna todas as atividades de um usuário em uma data específica
def get_activities_by_user_and_date(user_id: int, date: date_type) -> list[PhysicalActivity]:
    with use_session() as session:
        return (
            session.query(PhysicalActivity)
            .filter_by(user_id=user_id, date=date)
            .all()
        )


# Atualiza os campos de uma atividade existente pelo id
def update_activity(activity_id: int, **kwargs) -> PhysicalActivity | None:
    with use_session(commit=True) as session:
        activity = session.get(PhysicalActivity, activity_id)
        if activity is None:
            return None
        for key, value in kwargs.items():
            setattr(activity, key, value)
        session.flush()
        session.refresh(activity)
        return activity


# Remove uma atividade pelo id — retorna False se não existir
def delete_activity(activity_id: int) -> bool:
    with use_session(commit=True) as session:
        activity = session.get(PhysicalActivity, activity_id)
        if activity is None:
            return False
        session.delete(activity)
        return True


# Soma as calorias gastas de todas as atividades de um usuário em uma data
def get_total_calories_burned(user_id: int, date: date_type) -> float:
    with use_session() as session:
        activities = (
            session.query(PhysicalActivity)
            .filter_by(user_id=user_id, date=date)
            .all()
        )
        return sum(a.calories_burned or 0 for a in activities)
