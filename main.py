import tkinter as tk
from mvc.models import init_db
from mvc.ui_constants import COLORS
from mvc.views.create_account_view import CreateAccountView
from mvc.controllers.create_account_controller import CreateAccountController


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("DietTracker — Criar Conta")
        self.configure(bg=COLORS["bg"])
        self.geometry("660x520")
        self.resizable(False, False)

        init_db()

        self.view = CreateAccountView(self)
        self.controller = CreateAccountController(self.view)
        self.view.on_submit = self.controller.handle_submit
        self.view.on_cancel = self.quit
        self.view.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
