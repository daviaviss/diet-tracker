import tkinter as tk
from tkinter import messagebox

from mvc.ui_constants import COLORS, FONTS


class LoginView(tk.Frame):
    def __init__(self, master, on_submit=None, on_create_account=None):
        super().__init__(master, bg=COLORS["bg"])
        # Callbacks configurados pelo main.py após a criação da view
        self.on_submit = on_submit  # chamado ao clicar em "Entrar"
        self.on_create_account = on_create_account  # chamado ao clicar em "Criar conta"
        self.entries = {}  # dicionário que armazena os campos do formulário
        self._build_header()
        self._build_form()

    def _build_header(self):
        # Barra superior verde com o nome do app
        header = tk.Frame(self, bg=COLORS["primary"], height=45)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="DietTracker",
            fg=COLORS["white"],
            bg=COLORS["primary"],
            font=FONTS["header"],
        ).pack(side="left", padx=16)

        tk.Label(
            header,
            text="Acesse sua conta",
            fg=COLORS["white"],
            bg=COLORS["primary"],
            font=FONTS["header_nav"],
        ).place(relx=0.5, rely=0.5, anchor="center")

    def _build_form(self):
        # Frame externo ocupa o espaço restante abaixo do header
        outer = tk.Frame(self, bg=COLORS["bg"])
        outer.pack(fill="both", expand=True)

        # Card branco centralizado na tela (expand=True sem fill centraliza)
        card = tk.Frame(outer, bg=COLORS["white"])
        card.pack(expand=True)

        # Área interna do card com padding
        inner = tk.Frame(card, bg=COLORS["white"])
        inner.pack(padx=48, pady=36)

        # Título e subtítulo do card
        tk.Label(
            inner,
            text="DietTracker",
            bg=COLORS["white"],
            fg=COLORS["primary"],
            font=FONTS["title"],
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            inner,
            text="Gerencie seus hábitos alimentares",
            bg=COLORS["white"],
            fg=COLORS["text_light"],
            font=FONTS["small"],
            anchor="w",
        ).pack(anchor="w", pady=(2, 20))

        # Campo de e-mail
        self._label_required(inner, "E-mail")
        email_entry = tk.Entry(
            inner,
            font=FONTS["entry"],
            relief="solid",
            bd=1,
            highlightthickness=0,
            width=32,
        )
        email_entry.pack(fill="x", pady=(2, 14))
        self.entries["email"] = (
            email_entry  # registra no dicionário para leitura posterior
        )

        # Campo de senha (show="*" mascara os caracteres digitados)
        self._label_required(inner, "Senha")
        password_entry = tk.Entry(
            inner,
            font=FONTS["entry"],
            relief="solid",
            bd=1,
            show="*",
            highlightthickness=0,
            width=32,
        )
        password_entry.pack(fill="x", pady=(2, 24))
        self.entries["password"] = password_entry

        # Botão principal que aciona o processo de autenticação
        submit_btn = tk.Button(
            inner,
            text="Entrar",
            font=FONTS["button"],
            bg=COLORS["primary"],
            fg=COLORS["white"],
            activebackground=COLORS["primary_dark"],
            activeforeground=COLORS["white"],
            relief="flat",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=self._handle_submit,
        )
        submit_btn.pack(fill="x", pady=(0, 14))

        # Link de navegação para a tela de cadastro
        link_frame = tk.Frame(inner, bg=COLORS["white"])
        link_frame.pack()
        tk.Label(
            link_frame,
            text="Não possui conta?",
            bg=COLORS["white"],
            fg=COLORS["text_light"],
            font=FONTS["small"],
        ).pack(side="left")
        link = tk.Label(
            link_frame,
            text="Criar conta",
            bg=COLORS["white"],
            fg=COLORS["primary"],
            font=FONTS["small"],
            cursor="hand2",
        )
        link.pack(side="left")
        # Ao clicar no link, dispara o callback de navegação definido no main.py
        link.bind(
            "<Button-1>",
            lambda e: self.on_create_account() if self.on_create_account else None,
        )

    def _label_required(self, parent, text: str):
        # Tkinter não suporta cores parciais num Label, então usamos dois Labels lado a lado
        frame = tk.Frame(parent, bg=COLORS["white"])
        frame.pack(anchor="w")
        tk.Label(
            frame, text=text, bg=COLORS["white"], fg=COLORS["text"], font=FONTS["label"]
        ).pack(side="left")
        tk.Label(
            frame, text="*", bg=COLORS["white"], fg=COLORS["error"], font=FONTS["label"]
        ).pack(side="left")

    def _handle_submit(self):
        # Lê os dados do formulário e repassa ao controller via callback
        if self.on_submit:
            self.on_submit(self.get_form_data())

    def get_form_data(self) -> dict:
        # Retorna os valores dos campos como dicionário {"email": ..., "password": ...}
        return {key: widget.get() for key, widget in self.entries.items()}

    def show_error(self, message: str):
        messagebox.showerror("Erro", message)
