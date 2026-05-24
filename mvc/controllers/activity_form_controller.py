from datetime import datetime

from dao.physical_activity_dao import create_activity, update_activity


class ActivityFormController:

    def __init__(self, view, user, activity=None):
        self.view     = view
        self.user     = user
        self.activity = activity  # None = modo criação, PhysicalActivity = modo edição

    def handle_submit(self, data: dict):
        # Valida os campos antes de tentar salvar
        error = self._validate(data)
        if error:
            self.view.show_error(error)
            return

        try:
            # Converte os valores de texto para os tipos corretos
            date     = datetime.strptime(data["date"], "%d/%m/%Y").date()
            duration = int(data["duration"])
            calories = float(data["calories_burned"])

            if self.activity is None:
                # Criação: insere uma nova atividade no banco
                create_activity(
                    user_id=self.user.id,
                    name=data["name"],
                    date=date,
                    duration=duration,
                    calories_burned=calories,
                )
            else:
                # Edição: atualiza os campos da atividade existente
                # update_activity retorna None se o registro sumiu do banco entre
                # abrir o formulário e salvar (improvável, mas tratado por segurança)
                result = update_activity(
                    self.activity.id,
                    name=data["name"],
                    date=date,
                    duration=duration,
                    calories_burned=calories,
                )
                if result is None:
                    self.view.show_error("Atividade não encontrada. Ela pode ter sido excluída.")
                    return

            # Após salvar com sucesso, volta para a lista
            if self.view.on_cancel:
                self.view.on_cancel()

        except Exception as e:
            self.view.show_error(f"Erro ao salvar atividade: {e}")

    def _validate(self, data: dict) -> str | None:
        # Verifica se todos os campos obrigatórios foram preenchidos
        if not data["name"]:
            return "O nome da atividade é obrigatório."
        if not data["date"]:
            return "A data é obrigatória."
        if not data["duration"]:
            return "A duração é obrigatória."
        if not data["calories_burned"]:
            return "As calorias gastas são obrigatórias."

        # Valida o formato da data
        try:
            datetime.strptime(data["date"], "%d/%m/%Y")
        except ValueError:
            return "Data inválida. Use o formato DD/MM/AAAA."

        # Duração deve ser um inteiro positivo
        try:
            if int(data["duration"]) <= 0:
                raise ValueError
        except ValueError:
            return "Duração deve ser um número inteiro positivo."

        # Calorias devem ser um número positivo
        try:
            if float(data["calories_burned"]) < 0:
                raise ValueError
        except ValueError:
            return "Calorias gastas deve ser um número positivo."

        return None
