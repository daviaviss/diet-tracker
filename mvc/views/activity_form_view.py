import tkinter as tk
from datetime import date as date_type
from tkinter import messagebox

from mvc.ui_constants import COLORS, FONTS

# Texto exibido no campo Nome enquanto estiver vazio (placeholder manual)
_NAME_PLACEHOLDER = "ex.: Corrida, Musculação, Natação..."


class ActivityFormView(tk.Frame):

    def __init__(self, master, activity=None, on_submit=None, on_cancel=None):
        super().__init__(master, bg=COLORS["bg"])
        # Se activity for passada, o formulário entra em modo de edição (campos pré-preenchidos)
        # Se for None, o formulário entra em modo de criação (campos em branco)
        self._activity  = activity
        self.on_submit  = on_submit  # chamado ao clicar em "Salvar atividade"
        self.on_cancel  = on_cancel  # chamado ao clicar em "Cancelar" ou "← Voltar"
        self.entries    = {}         # dicionário com os campos do formulário para leitura posterior

        self._build_header()
        self._build_body()

        # Se estiver editando, preenche os campos com os dados existentes
        if activity:
            self._populate(activity)

    def _build_header(self):
        header = tk.Frame(self, bg=COLORS["primary"], height=45)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="DietTracker",
            fg=COLORS["white"], bg=COLORS["primary"], font=FONTS["header"],
        ).pack(side="left", padx=16)

        # Título muda conforme o modo (criar ou editar)
        title = "Editar Atividade" if self._activity else "Nova Atividade Física"
        tk.Label(
            header, text=title,
            fg=COLORS["white"], bg=COLORS["primary"], font=FONTS["header_nav"],
        ).place(relx=0.5, rely=0.5, anchor="center")

        back = tk.Label(
            header, text="← Voltar",
            fg=COLORS["white"], bg=COLORS["primary"], font=FONTS["header_nav"], cursor="hand2",
        )
        back.pack(side="right", padx=16)
        back.bind("<Button-1>", lambda e: self.on_cancel() if self.on_cancel else None)

    def _build_body(self):
        outer = tk.Frame(self, bg=COLORS["bg"])
        outer.pack(fill="both", expand=True, padx=24, pady=(16, 16))

        card = tk.Frame(outer, bg=COLORS["white"])
        card.pack(fill="both", expand=True)

        inner = tk.Frame(card, bg=COLORS["white"])
        inner.pack(fill="both", expand=True, padx=28, pady=20)

        # Título muda conforme o modo: criação ou edição
        form_title = "Edição de atividade física" if self._activity else "Cadastro de atividade física"
        tk.Label(
            inner, text=form_title,
            bg=COLORS["white"], fg=COLORS["text"], font=FONTS["title"], anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        # --- Nome da atividade (ocupa as 2 colunas) ---
        self._add_label(inner, "Nome da atividade", required=True, row=1, col=0, colspan=2)

        # Frame faz o papel da borda, permitindo padx interno no Entry
        # (tk.Entry não tem padding de texto nativo — o wrapper resolve isso)
        name_frame = tk.Frame(inner, bg=COLORS["white"], relief="solid", bd=1)
        name_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        name_entry = tk.Entry(
            name_frame, font=FONTS["entry"], relief="flat", bd=0,
            highlightthickness=0, fg=COLORS["text_light"], bg=COLORS["white"],
        )
        # Exibe o placeholder quando o campo está vazio
        name_entry.insert(0, _NAME_PLACEHOLDER)
        name_entry.pack(fill="x", padx=6, pady=3)
        name_entry.bind("<FocusIn>",  lambda e: self._clear_placeholder(name_entry, _NAME_PLACEHOLDER))
        name_entry.bind("<FocusOut>", lambda e: self._restore_placeholder(name_entry, _NAME_PLACEHOLDER))
        self.entries["name"] = name_entry

        # --- Data (coluna esquerda) e Duração (coluna direita) na mesma linha ---
        self._add_label(inner, "Data", required=True, row=3, col=0)
        date_entry = tk.Entry(inner, font=FONTS["entry"], relief="solid", bd=1, highlightthickness=0)
        # Preenche a data com hoje como padrão
        date_entry.insert(0, date_type.today().strftime("%d/%m/%Y"))
        date_entry.grid(row=4, column=0, sticky="ew", padx=(0, 12), pady=(0, 12))
        self.entries["date"] = date_entry

        self._add_label(inner, "Duração (minutos)", required=True, row=3, col=1)
        duration_entry = tk.Entry(inner, font=FONTS["entry"], relief="solid", bd=1, highlightthickness=0)
        duration_entry.grid(row=4, column=1, sticky="ew", pady=(0, 12))
        self.entries["duration"] = duration_entry

        # --- Calorias gastas (apenas coluna esquerda, conforme protótipo) ---
        self._add_label(inner, "Calorias gastas (kcal)", required=True, row=5, col=0)
        calories_entry = tk.Entry(inner, font=FONTS["entry"], relief="solid", bd=1, highlightthickness=0)
        calories_entry.grid(row=6, column=0, sticky="ew", padx=(0, 12), pady=(0, 12))
        self.entries["calories_burned"] = calories_entry

        # --- Barra informativa ---
        info_bar = tk.Frame(inner, bg=COLORS["white"])
        info_bar.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(4, 16))

        tk.Frame(info_bar, bg=COLORS["primary"], width=4).pack(side="left", fill="y")
        tk.Label(
            info_bar,
            text="  As calorias informadas serão automaticamente descontadas do saldo do dia.",
            bg=COLORS["info_bg"], fg=COLORS["text"], font=FONTS["small"], anchor="w",
        ).pack(side="left", fill="x", expand=True, ipady=8)

        # --- Botões alinhados à direita ---
        btn_row = tk.Frame(inner, bg=COLORS["white"])
        btn_row.grid(row=8, column=0, columnspan=2, sticky="e")

        tk.Button(
            btn_row, text="Cancelar",
            font=FONTS["button"],
            bg=COLORS["button_cancel_bg"], fg=COLORS["button_cancel_fg"],
            relief="solid", bd=1, padx=16, pady=6, cursor="hand2",
            command=lambda: self.on_cancel() if self.on_cancel else None,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            btn_row, text="Salvar atividade",
            font=FONTS["button"],
            bg=COLORS["primary"], fg=COLORS["white"],
            activebackground=COLORS["primary_dark"], activeforeground=COLORS["white"],
            relief="flat", bd=0, padx=16, pady=6, cursor="hand2",
            command=self._handle_submit,
        ).pack(side="left")

        # As 2 colunas crescem igualmente quando a janela for redimensionada
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)

    def _add_label(self, parent, text: str, required: bool, row: int, col: int, colspan: int = 1):
        # Coloca o texto do label e o asterisco vermelho em frames separados lado a lado
        # (mesma técnica usada em login_view.py para colorir apenas o asterisco de vermelho)
        frame = tk.Frame(parent, bg=COLORS["white"])
        frame.grid(row=row, column=col, columnspan=colspan, sticky="w", pady=(0, 2))
        tk.Label(
            frame, text=text,
            bg=COLORS["white"], fg=COLORS["text"], font=FONTS["label"],
        ).pack(side="left")
        if required:
            tk.Label(
                frame, text="*",
                bg=COLORS["white"], fg=COLORS["error"], font=FONTS["label"],
            ).pack(side="left")

    def _clear_placeholder(self, widget: tk.Entry, placeholder: str):
        # Remove o placeholder quando o usuário clica no campo
        if widget.get() == placeholder:
            widget.delete(0, "end")
            widget.config(fg=COLORS["text"])

    def _restore_placeholder(self, widget: tk.Entry, placeholder: str):
        # Restaura o placeholder se o usuário sair do campo sem digitar nada
        if not widget.get():
            widget.insert(0, placeholder)
            widget.config(fg=COLORS["text_light"])

    def _populate(self, activity):
        # Preenche o formulário com os dados da atividade existente (modo edição)
        name_entry = self.entries["name"]
        name_entry.delete(0, "end")
        name_entry.insert(0, activity.name)
        name_entry.config(fg=COLORS["text"])

        self.entries["date"].delete(0, "end")
        self.entries["date"].insert(0, activity.date.strftime("%d/%m/%Y"))

        self.entries["duration"].delete(0, "end")
        self.entries["duration"].insert(0, str(activity.duration))

        self.entries["calories_burned"].delete(0, "end")
        self.entries["calories_burned"].insert(0, str(int(activity.calories_burned)))

    def _handle_submit(self):
        if self.on_submit:
            self.on_submit(self.get_form_data())

    def get_form_data(self) -> dict:
        # Lê todos os campos e retorna como dicionário para o controller validar
        name = self.entries["name"].get()
        # Ignora o placeholder: se ainda estiver lá, o campo está vazio
        if name == _NAME_PLACEHOLDER:
            name = ""
        return {
            "name":           name.strip(),
            "date":           self.entries["date"].get().strip(),
            "duration":       self.entries["duration"].get().strip(),
            "calories_burned": self.entries["calories_burned"].get().strip(),
        }

    def show_error(self, message: str):
        messagebox.showerror("Erro", message)
