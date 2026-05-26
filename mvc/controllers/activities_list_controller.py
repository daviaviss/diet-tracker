from datetime import date as date_type, datetime

from dao.physical_activity_dao import (
    delete_activity,
    get_activities_by_user_and_date,
    get_total_calories_burned,
)


class ActivitiesListController:

    def __init__(self, view, user):
        self.view = view
        self.user = user
        self._changing_date = False

    def load(self, date: date_type | None = None):
        # Carrega as atividades da data informada (padrão: hoje)
        # e passa a lista e o total de calorias para a view renderizar
        if date is None:
            date = date_type.today()
        activities    = get_activities_by_user_and_date(self.user.id, date)
        total_calories = get_total_calories_burned(self.user.id, date)
        self.view.load_activities(activities, total_calories)

    def handle_date_change(self, date_str: str):
        # O messagebox dispara FocusOut no Entry, o que chamaria este método de novo.
        # O flag evita que a segunda chamada cause um erro duplicado.
        if self._changing_date:
            return
        self._changing_date = True
        try:
            date = datetime.strptime(date_str, "%d/%m/%Y").date()
            self.load(date)
        except ValueError:
            self.view.show_error("Data inválida. Use o formato DD/MM/AAAA.")
            today = date_type.today()
            self.view.set_date(today.strftime("%d/%m/%Y"))
            self.load(today)
        finally:
            self._changing_date = False

    def handle_delete(self, activity):
        # Pede confirmação antes de apagar (ação irreversível)
        confirmed = self.view.show_confirm(f"Deseja excluir '{activity.name}'?")
        if not confirmed:
            return

        try:
            delete_activity(activity.id)
        except Exception:
            self.view.show_error("Não foi possível excluir a atividade. Tente novamente.")
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
