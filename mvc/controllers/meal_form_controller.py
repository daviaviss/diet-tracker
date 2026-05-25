from datetime import datetime

from mvc.ui_constants import MEAL_CATEGORY_OPTIONS, DIET_STATUS_OPTIONS
from mvc.models.meal_category import MealCategory
from mvc.models.diet_status import DietStatus
from dao.meal_dao import create_meal, update_meal, get_meal_by_user_date_category


class MealFormController:

    def __init__(self, view, user, meal=None):
        self.view = view
        self.user = user
        self.meal = meal  # None = modo criação, Meal = modo edição

    def handle_submit(self, data: dict):
        # Valida os campos antes de tentar salvar
        error = self._validate(data)
        if error:
            self.view.show_error(error)
            return

        try:
            # Converte os valores de texto para os tipos corretos
            date = datetime.strptime(data["date"], "%d/%m/%Y").date()
            time = datetime.strptime(data["time"], "%H:%M").time()
            calories = float(data["calories"])
            protein = float(data["protein"])
            carbs = float(data["carbs"])
            fat = float(data["fat"])
            category_value = self._resolve_category(data["category"])
            status_value = self._resolve_status(data["status"])

            if self.meal is None:
                # Criação: insere uma nova refeição no banco
                create_meal(
                    user_id=self.user.id,
                    name=data["name"],
                    category=category_value,
                    status=status_value,
                    date=date,
                    time=time,
                    calories=calories,
                    protein=protein,
                    carbs=carbs,
                    fat=fat,
                )
            else:
                # Edição: atualiza os campos da refeição existente
                result = update_meal(
                    self.meal.id,
                    name=data["name"],
                    category=category_value,
                    status=status_value,
                    date=date,
                    time=time,
                    calories=calories,
                    protein=protein,
                    carbs=carbs,
                    fat=fat,
                )
                if result is None:
                    self.view.show_error("Refeição não encontrada. Ela pode ter sido excluída.")
                    return

            # Após salvar com sucesso, volta para a lista
            if self.view.on_cancel:
                self.view.on_cancel()

        except Exception:
            self.view.show_error("Não foi possível salvar a refeição. Tente novamente.")

    def _validate(self, data: dict) -> str | None:
        # Verifica se todos os campos obrigatórios foram preenchidos
        if not data["name"]:
            return "O nome da refeição é obrigatório."
        if not data["date"]:
            return "A data é obrigatória."
        if not data["time"]:
            return "O horário é obrigatório."
        if not data["calories"]:
            return "As calorias são obrigatórias."
        if not data["protein"]:
            return "As proteínas são obrigatórias."
        if not data["carbs"]:
            return "Os carboidratos são obrigatórios."
        if not data["fat"]:
            return "As gorduras são obrigatórias."

        # Valida o formato da data
        try:
            date = datetime.strptime(data["date"], "%d/%m/%Y").date()
        except ValueError:
            return "Data inválida. Use o formato DD/MM/AAAA."

        # Valida o formato do horário
        try:
            datetime.strptime(data["time"], "%H:%M")
        except ValueError:
            return "Horário inválido. Use o formato HH:MM."

        # Calorias devem ser um número positivo
        try:
            if float(data["calories"]) < 0:
                raise ValueError
        except ValueError:
            return "Calorias deve ser um número positivo."

        # Macronutrientes devem ser números não negativos
        try:
            if float(data["protein"]) < 0:
                raise ValueError
        except ValueError:
            return "Proteínas deve ser um número não negativo."

        try:
            if float(data["carbs"]) < 0:
                raise ValueError
        except ValueError:
            return "Carboidratos deve ser um número não negativo."

        try:
            if float(data["fat"]) < 0:
                raise ValueError
        except ValueError:
            return "Gorduras deve ser um número não negativo."

        # RN001: não é permitido cadastrar duas refeições da mesma categoria no mesmo dia
        category_value = self._resolve_category(data["category"])
        try:
            existing = get_meal_by_user_date_category(self.user.id, date, category_value)
        except Exception:
            return "Não foi possível verificar a categoria. Tente novamente."

        if existing:
            # Se estiver editando a mesma refeição, permite manter a categoria
            if self.meal is not None and existing.id == self.meal.id:
                pass
            else:
                return "RN001: não é permitido cadastrar duas refeições da mesma categoria no mesmo dia."

        return None

    def _resolve_category(self, label: str) -> MealCategory:
        for text, value in MEAL_CATEGORY_OPTIONS:
            if text == label:
                return MealCategory(value)
        return MealCategory.BREAKFAST

    def _resolve_status(self, label: str) -> DietStatus:
        for text, value in DIET_STATUS_OPTIONS:
            if text == label:
                return DietStatus(value)
        return DietStatus.ON_DIET
