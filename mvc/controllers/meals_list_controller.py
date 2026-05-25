from datetime import date as date_type, datetime

from dao.meal_dao import (
    delete_meal,
    get_meals_by_user_and_date,
    get_total_calories,
)
from dao.physical_activity_dao import get_total_calories_burned


class MealsListController:

    def __init__(self, view, user):
        self.view = view
        self.user = user

    def load(self, date: date_type | None = None):
        # Carrega as refeições da data informada (padrão: hoje)
        # e passa a lista e o total líquido de calorias para a view renderizar
        if date is None:
            date = date_type.today()
        meals = get_meals_by_user_and_date(self.user.id, date)
        # Total do dia = calorias das refeições − calorias gastas em atividades
        meal_calories = get_total_calories(self.user.id, date)
        activity_calories = get_total_calories_burned(self.user.id, date)
        net_total = meal_calories - activity_calories
        self.view.load_meals(meals, net_total)

    def handle_date_change(self, date_str: str):
        # Converte a string digitada pelo usuário e recarrega a lista
        try:
            date = datetime.strptime(date_str, "%d/%m/%Y").date()
            self.load(date)
        except ValueError:
            self.view.show_error("Data inválida. Use o formato DD/MM/AAAA.")

    def handle_delete(self, meal):
        # Pede confirmação antes de apagar (ação irreversível)
        confirmed = self.view.show_confirm(f"Deseja excluir '{meal.name}'?")
        if not confirmed:
            return

        try:
            delete_meal(meal.id)
        except Exception:
            self.view.show_error("Não foi possível excluir a refeição. Tente novamente.")
            return

        # Recarrega a lista com a data atual do filtro após excluir
        self._reload_current_date()

    def _reload_current_date(self):
        # Reutiliza a data já digitada no campo de filtro para recarregar a lista
        date_str = self.view.get_date_str()
        try:
            date = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            date = date_type.today()
        self.load(date)
