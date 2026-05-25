from mvc.ui_constants import ACTIVITY_FACTORS, GOAL_OPTIONS
from mvc.models.nutritional_goal import NutritionalGoal
from dao.user_dao import create_user, get_user_by_email


class CreateAccountController:

    def __init__(self, view):
        self.view = view
        # Callback chamado após o cadastro bem-sucedido — configurado pelo NavigationController
        self.on_success = None

    def handle_submit(self, data: dict):
        error = self._validate(data)
        if error:
            self.view.show_error(error)
            return

        activity_value = self._resolve_activity_factor(data["activity_factor"])
        goal_value = self._resolve_goal(data["goal"])

        try:
            create_user(
                name=data["name"],
                email=data["email"].strip(),
                password=data["password"],
                age=int(data["age"]),
                weight=float(data["weight"]),
                height=float(data["height"]),
                activity_factor=activity_value,
                goal=goal_value,
            )
            self.view.show_success("Conta criada com sucesso!")
            if self.on_success:
                self.on_success()
        except Exception:
            self.view.show_error(
                "Não foi possível criar a conta. Tente novamente mais tarde."
            )

    def _validate(self, data: dict) -> str | None:
        required = ["name", "email", "password", "password_confirm", "age", "weight", "height"]
        for field in required:
            if not data.get(field, "").strip():
                return "Todos os campos obrigatórios devem ser preenchidos."

        # Valida formato básico de e-mail
        email = data["email"].strip()
        if "@" not in email or "." not in email.split("@")[-1]:
            return "Informe um e-mail válido."

        # Verifica se o e-mail já está cadastrado antes de tentar criar
        try:
            existing = get_user_by_email(email)
        except Exception:
            return "Não foi possível verificar o e-mail. Tente novamente."
        if existing:
            return "Este e-mail já está cadastrado."

        if data["password"] != data["password_confirm"]:
            return "As senhas não coincidem."

        try:
            int(data["age"])
        except ValueError:
            return "Idade deve ser um número inteiro."

        try:
            float(data["weight"])
            float(data["height"])
        except ValueError:
            return "Peso e altura devem ser números válidos."

        return None

    def _resolve_activity_factor(self, label: str) -> float:
        for text, value in ACTIVITY_FACTORS:
            if text == label:
                return value
        return 1.2

    def _resolve_goal(self, label: str) -> NutritionalGoal:
        for text, value in GOAL_OPTIONS:
            if text == label:
                return NutritionalGoal(value)
        return NutritionalGoal.LOSE_WEIGHT

    def _clear_form(self):
        for key, widget in self.view.entries.items():
            if hasattr(widget, "delete"):
                widget.delete(0, "end")
            elif hasattr(widget, "set"):
                widget.set("")
