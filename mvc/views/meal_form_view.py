import tkinter as tk
from datetime import date as date_type
from tkinter import ttk, messagebox

from mvc.ui_constants import COLORS, FONTS, MEAL_CATEGORY_OPTIONS, DIET_STATUS_OPTIONS

# Texto exibido no campo Nome enquanto estiver vazio (placeholder manual)
_NAME_PLACEHOLDER = "Arroz integral, frango grelhado, salada de folhas"


class MealFormView(tk.Frame):

    def __init__(self, master, meal=None, on_submit=None, on_cancel=None):
        super().__init__(master, bg=COLORS["bg"])
        # Se meal for passado, o formulário entra em modo de edição (campos pré-preenchidos)
        # Se for None, o formulário entra em modo de criação (campos em branco)
        self._meal      = meal
        self.on_submit  = on_submit   # chamado ao clicar em "Salvar refeição"
        self.on_cancel  = on_cancel   # chamado ao clicar em "Cancelar" ou "← Voltar"
        self.entries    = {}          # dicionário com os campos do formulário para leitura posterior

        self._build_header()
        self._build_body()

        # Se estiver editando, preenche os campos com os dados existentes
        if meal:
            self._populate(meal)

    def _build_header(self):
        header = tk.Frame(self, bg=COLORS["primary"], height=45)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="DietTracker",
            fg=COLORS["white"], bg=COLORS["primary"], font=FONTS["header"],
        ).pack(side="left", padx=16)

        # Título muda conforme o modo (criar ou editar)
        title = "Editar Refeição" if self._meal else "Nova Refeição"
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
        # --- Botões fora do card, fixos na parte inferior da tela ---
        btn_bar = tk.Frame(self, bg=COLORS["bg"])
        btn_bar.pack(side="bottom", fill="x", padx=24, pady=(0, 16))

        btn_frame = tk.Frame(btn_bar, bg=COLORS["bg"])
        btn_frame.pack(side="right")

        tk.Button(
            btn_frame, text="Cancelar",
            font=FONTS["button"],
            bg=COLORS["button_cancel_bg"], fg=COLORS["button_cancel_fg"],
            relief="solid", bd=1, padx=16, pady=6, cursor="hand2",
            command=lambda: self.on_cancel() if self.on_cancel else None,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            btn_frame, text="Salvar refeição",
            font=FONTS["button"],
            bg=COLORS["primary"], fg=COLORS["white"],
            activebackground=COLORS["primary_dark"], activeforeground=COLORS["white"],
            relief="flat", bd=0, padx=16, pady=6, cursor="hand2",
            command=self._handle_submit,
        ).pack(side="left")

        outer = tk.Frame(self, bg=COLORS["bg"])
        outer.pack(fill="both", expand=True, padx=24, pady=(16, 8))

        card = tk.Frame(outer, bg=COLORS["white"])
        card.pack(fill="both", expand=True)

        inner = tk.Frame(card, bg=COLORS["white"])
        inner.pack(fill="both", expand=True, padx=28, pady=20)

        # Título muda conforme o modo: criação ou edição
        form_title = "Edição de refeição" if self._meal else "Cadastro de refeição"
        tk.Label(
            inner, text=form_title,
            bg=COLORS["white"], fg=COLORS["text"], font=FONTS["title"], anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        # --- Categoria (coluna esquerda) e Status (coluna direita) ---
        self._add_label(inner, "Categoria", required=True, row=1, col=0)
        cat_var = tk.StringVar(value=MEAL_CATEGORY_OPTIONS[0][0])
        cat_combo = ttk.Combobox(
            inner, textvariable=cat_var,
            values=[label for label, _ in MEAL_CATEGORY_OPTIONS],
            font=FONTS["entry"], state="readonly",
        )
        cat_combo.grid(row=2, column=0, sticky="ew", padx=(0, 12), pady=(0, 8))
        self.entries["category"] = cat_var

        self._add_label(inner, "Status", required=True, row=1, col=1)
        status_var = tk.StringVar(value=DIET_STATUS_OPTIONS[0][0])
        status_combo = ttk.Combobox(
            inner, textvariable=status_var,
            values=[label for label, _ in DIET_STATUS_OPTIONS],
            font=FONTS["entry"], state="readonly",
        )
        status_combo.grid(row=2, column=1, sticky="ew", pady=(0, 8))
        self.entries["status"] = status_var

        # --- Data (coluna esquerda) e Horário (coluna direita) ---
        self._add_label(inner, "Data", required=True, row=3, col=0)
        date_entry = tk.Entry(inner, font=FONTS["entry"], relief="solid", bd=1, highlightthickness=0)
        # Preenche a data com hoje como padrão
        date_entry.insert(0, date_type.today().strftime("%d/%m/%Y"))
        date_entry.grid(row=4, column=0, sticky="ew", padx=(0, 12), pady=(0, 8))
        self.entries["date"] = date_entry

        self._add_label(inner, "Horário", required=True, row=3, col=1)
        time_entry = tk.Entry(inner, font=FONTS["entry"], relief="solid", bd=1, highlightthickness=0)
        time_entry.grid(row=4, column=1, sticky="ew", pady=(0, 8))
        self.entries["time"] = time_entry

        # --- Nome (ocupa as 2 colunas) ---
        self._add_label(inner, "Nome", required=True, row=5, col=0, colspan=2)

        name_entry = tk.Entry(
            inner, font=FONTS["entry"], relief="solid", bd=1,
            highlightthickness=0, fg=COLORS["text_light"],
        )
        # Exibe o placeholder quando o campo está vazio
        name_entry.insert(0, _NAME_PLACEHOLDER)
        name_entry.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        name_entry.bind("<FocusIn>",  lambda e: self._clear_placeholder(name_entry, _NAME_PLACEHOLDER))
        name_entry.bind("<FocusOut>", lambda e: self._restore_placeholder(name_entry, _NAME_PLACEHOLDER))
        self.entries["name"] = name_entry

        # --- Calorias (coluna esquerda, conforme protótipo) ---
        self._add_label(inner, "Calorias (kcal)", required=True, row=7, col=0)
        calories_entry = tk.Entry(inner, font=FONTS["entry"], relief="solid", bd=1, highlightthickness=0)
        calories_entry.grid(row=8, column=0, sticky="w", padx=(0, 12), pady=(0, 8), ipadx=60)
        self.entries["calories"] = calories_entry

        # --- Macronutrientes (g) — 3 campos lado a lado ---
        macro_label = tk.Frame(inner, bg=COLORS["white"])
        macro_label.grid(row=9, column=0, columnspan=2, sticky="w", pady=(0, 2))
        tk.Label(
            macro_label, text="Macronutrientes (g)",
            bg=COLORS["white"], fg=COLORS["text"], font=FONTS["label_bold"],
        ).pack(side="left")

        macro_row = tk.Frame(inner, bg=COLORS["white"])
        macro_row.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        macro_row.columnconfigure(0, weight=1)
        macro_row.columnconfigure(1, weight=1)
        macro_row.columnconfigure(2, weight=1)

        # Proteínas
        tk.Label(
            macro_row, text="Proteínas *",
            bg=COLORS["white"], fg=COLORS["text"], font=FONTS["small"],
        ).grid(row=0, column=0, sticky="w", padx=(0, 8))
        protein_entry = tk.Entry(macro_row, font=FONTS["entry"], relief="solid", bd=1, highlightthickness=0)
        protein_entry.grid(row=1, column=0, sticky="ew", padx=(0, 8))
        self.entries["protein"] = protein_entry

        # Carboidratos
        tk.Label(
            macro_row, text="Carboidratos *",
            bg=COLORS["white"], fg=COLORS["text"], font=FONTS["small"],
        ).grid(row=0, column=1, sticky="w", padx=(0, 8))
        carbs_entry = tk.Entry(macro_row, font=FONTS["entry"], relief="solid", bd=1, highlightthickness=0)
        carbs_entry.grid(row=1, column=1, sticky="ew", padx=(0, 8))
        self.entries["carbs"] = carbs_entry

        # Gorduras
        tk.Label(
            macro_row, text="Gorduras *",
            bg=COLORS["white"], fg=COLORS["text"], font=FONTS["small"],
        ).grid(row=0, column=2, sticky="w")
        fat_entry = tk.Entry(macro_row, font=FONTS["entry"], relief="solid", bd=1, highlightthickness=0)
        fat_entry.grid(row=1, column=2, sticky="ew")
        self.entries["fat"] = fat_entry

        # --- Barra informativa (RN001) ---
        info_bar = tk.Frame(inner, bg=COLORS["white"])
        info_bar.grid(row=11, column=0, columnspan=2, sticky="ew", pady=(4, 8))

        tk.Frame(info_bar, bg=COLORS["error"], width=4).pack(side="left", fill="y")
        tk.Label(
            info_bar,
            text="  RN001: não é permitido cadastrar duas refeições da mesma categoria no mesmo dia.",
            bg=COLORS["info_bg"], fg=COLORS["error"], font=FONTS["small"], anchor="w",
        ).pack(side="left", fill="x", expand=True, ipady=6)

        # As 2 colunas crescem igualmente quando a janela for redimensionada
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)

    def _add_label(self, parent, text: str, required: bool, row: int, col: int, colspan: int = 1):
        # Coloca o texto do label e o asterisco vermelho em frames separados lado a lado
        frame = tk.Frame(parent, bg=COLORS["white"])
        frame.grid(row=row, column=col, columnspan=colspan, sticky="w", pady=(0, 2))
        tk.Label(
            frame, text=text,
            bg=COLORS["white"], fg=COLORS["text"], font=FONTS["label"],
        ).pack(side="left")
        if required:
            tk.Label(
                frame, text=" *",
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

    def _populate(self, meal):
        # Preenche o formulário com os dados da refeição existente (modo edição)

        # Categoria
        for label, value in MEAL_CATEGORY_OPTIONS:
            if meal.category and meal.category.value == value:
                self.entries["category"].set(label)
                break

        # Status
        for label, value in DIET_STATUS_OPTIONS:
            if meal.status and meal.status.value == value:
                self.entries["status"].set(label)
                break

        # Data
        self.entries["date"].delete(0, "end")
        self.entries["date"].insert(0, meal.date.strftime("%d/%m/%Y"))

        # Horário
        self.entries["time"].delete(0, "end")
        if meal.time:
            self.entries["time"].insert(0, meal.time.strftime("%H:%M"))

        # Nome
        name_entry = self.entries["name"]
        name_entry.delete(0, "end")
        name_entry.insert(0, meal.name)
        name_entry.config(fg=COLORS["text"])

        # Calorias
        self.entries["calories"].delete(0, "end")
        if meal.calories is not None:
            self.entries["calories"].insert(0, str(int(meal.calories)))

        # Macronutrientes
        self.entries["protein"].delete(0, "end")
        if meal.protein is not None:
            self.entries["protein"].insert(0, str(int(meal.protein)))

        self.entries["carbs"].delete(0, "end")
        if meal.carbs is not None:
            self.entries["carbs"].insert(0, str(int(meal.carbs)))

        self.entries["fat"].delete(0, "end")
        if meal.fat is not None:
            self.entries["fat"].insert(0, str(int(meal.fat)))

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
            "category":   self.entries["category"].get(),
            "status":     self.entries["status"].get(),
            "date":       self.entries["date"].get().strip(),
            "time":       self.entries["time"].get().strip(),
            "name":       name.strip(),
            "calories":   self.entries["calories"].get().strip(),
            "protein":    self.entries["protein"].get().strip(),
            "carbs":      self.entries["carbs"].get().strip(),
            "fat":        self.entries["fat"].get().strip(),
        }

    def show_error(self, message: str):
        messagebox.showerror("Erro", message)

    def show_success(self, message: str):
        messagebox.showinfo("Sucesso", message)
