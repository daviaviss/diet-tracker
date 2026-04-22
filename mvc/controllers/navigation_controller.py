from tkinter import messagebox

from mvc.controllers.create_account_controller import CreateAccountController
from mvc.controllers.login_controller import LoginController
from mvc.views.create_account_view import CreateAccountView
from mvc.views.login_view import LoginView


class NavigationController:
    """Responsável por trocar as telas da janela principal."""

    def __init__(self, root):
        self.root = root
        self._current = None  # frame ativo no momento

    def _swap(self, view):
        # Destrói a tela atual antes de exibir a nova
        if self._current:
            self._current.destroy()
        self._current = view
        view.pack(fill="both", expand=True)

    def show_login(self):
        view = LoginView(self.root)
        ctrl = LoginController(view)
        view.on_submit = ctrl.handle_submit
        view.on_create_account = self.show_create_account  # "Criar conta" - UC01
        ctrl.on_success = self.show_home  # login ok → próxima tela
        self._swap(view)

    def show_create_account(self):
        view = CreateAccountView(self.root, on_cancel=self.show_login)
        ctrl = CreateAccountController(view)
        view.on_submit = ctrl.handle_submit
        self._swap(view)

    def show_home(self, user):
        # UC03 — será substituído pela tela Home
        messagebox.showinfo("Bem-vindo", f"Bem-vindo, {user.name}!")
