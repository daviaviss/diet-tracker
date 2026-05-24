from tkinter import messagebox


class HomeController:

    def __init__(self, view, user):
        self.view = view
        self.user = user
        # Dicionário de callbacks de navegação, preenchido pelo NavigationController
        # após a criação. Cada chave é uma seção (ex: "activities") e o valor é a
        # função que deve ser chamada para abrir aquela tela.
        self.on_navigate_to: dict = {}

    def handle_navigate(self, section: str):
        # Busca o handler da seção clicada; se não existir ainda, exibe aviso
        handler = self.on_navigate_to.get(section)
        if handler:
            handler()
        else:
            messagebox.showinfo("Em breve", f"Funcionalidade '{section}' ainda não implementada.")
