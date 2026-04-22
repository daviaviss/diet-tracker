from typing import Callable

from dao.user_dao import get_user_by_email, verify_password


class LoginController:
    """Responsável por controlar o login do usuário."""

    def __init__(self, view):
        # Guarda referência à view para poder exibir erros
        self.view = view
        # Callback definido pelo main.py — é chamado quando o login é bem-sucedido
        self.on_success: Callable | None = None

    def handle_submit(self, data: dict):
        # Primeiro valida se os campos foram preenchidos
        error = self._validate(data)
        if error:
            self.view.show_error(error)
            return

        # Busca o usuário no banco pelo e-mail informado
        user = get_user_by_email(data["email"].strip())

        # Se o usuário não existir ou a senha estiver errada, exibe erro genérico
        # (mensagem propositalmente vaga para não revelar qual campo está errado)
        if not user or not verify_password(data["password"], str(user.password)):
            self.view.show_error("E-mail ou senha incorretos.")
            return

        # Login bem-sucedido: dispara o callback passando o objeto User
        if self.on_success:
            self.on_success(user)

    def _validate(self, data: dict) -> str | None:
        email = data.get("email", "").strip()
        password = data.get("password", "")

        # Verifica se ambos estão vazios antes de checar individualmente
        if not email and not password:
            return "Preencha o e-mail e a senha para continuar."
        if not email:
            return "O campo e-mail é obrigatório."
        if not password:
            return "O campo senha é obrigatório."

        # Valida formato básico de e-mail (deve conter @ e pelo menos um ponto após ele)
        if "@" not in email or "." not in email.split("@")[-1]:
            return "Informe um e-mail válido."

        return None
