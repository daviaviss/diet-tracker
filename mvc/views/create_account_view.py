import tkinter as tk
from tkinter import ttk, messagebox
from mvc.ui_constants import COLORS, FONTS, ACTIVITY_FACTORS, GOAL_OPTIONS, SEX_OPTIONS


class CreateAccountView(tk.Frame):

    def __init__(self, master, on_submit=None, on_cancel=None):
        super().__init__(master, bg=COLORS["bg"])
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        self.entries = {}
        self._build_header()
        self._build_form()
        self._build_buttons()

    def _build_header(self):
        header = tk.Frame(self, bg=COLORS["primary"], height=45)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="DietTracker", fg=COLORS["white"],
            bg=COLORS["primary"], font=FONTS["header"],
        ).pack(side="left", padx=16)

        tk.Label(
            header, text="Criar Conta", fg=COLORS["white"],
            bg=COLORS["primary"], font=FONTS["header_nav"],
        ).pack(side="left", expand=True)

        back_btn = tk.Label(
            header, text="← Voltar", fg=COLORS["white"],
            bg=COLORS["primary"], font=FONTS["header_nav"], cursor="hand2",
        )
        back_btn.pack(side="right", padx=16)
        back_btn.bind("<Button-1>", lambda e: self.on_cancel() if self.on_cancel else None)

    def _build_form(self):
        outer = tk.Frame(self, bg=COLORS["bg"])
        outer.pack(fill="both", expand=True, padx=24, pady=(16, 8))

        form = tk.Frame(outer, bg=COLORS["white"], bd=0, relief="flat")
        form.pack(fill="both", expand=True)

        inner = tk.Frame(form, bg=COLORS["white"])
        inner.pack(fill="both", expand=True, padx=28, pady=20)

        tk.Label(
            inner, text="Cadastre-se no DietTracker",
            bg=COLORS["white"], fg=COLORS["text"], font=FONTS["title"], anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        fields = [
            [
                ("Nome completo *", "name", "entry", None),
                ("E-mail *", "email", "entry", "usado no login"),
            ],
            [
                ("Senha *", "password", "password", None),
                ("Confirmar senha *", "password_confirm", "password", None),
            ],
            [
                ("Idade (anos) *", "age", "entry", "ex.: 25"),
                ("Sexo *", "sex", "combo", SEX_OPTIONS),
            ],
            [
                ("Peso (kg) *", "weight", "entry", None),
                ("Altura (cm) *", "height", "entry", None),
            ],
            [
                ("Fator de atividade *", "activity_factor", "combo",
                 [label for label, _ in ACTIVITY_FACTORS]),
                ("Objetivo nutricional *", "goal", "combo",
                 [label for label, _ in GOAL_OPTIONS]),
            ],
        ]

        row_idx = 1
        for row_fields in fields:
            for col, (label_text, key, field_type, extra) in enumerate(row_fields):
                self._add_field(inner, row_idx, col, label_text, key, field_type, extra)
            row_idx += 2

        inner.columnconfigure(0, weight=1, uniform="col")
        inner.columnconfigure(1, weight=1, uniform="col")

    def _add_field(self, parent, row, col, label_text, key, field_type, extra):
        padx = (0, 12) if col == 0 else (12, 0)

        tk.Label(
            parent, text=label_text, bg=COLORS["white"],
            fg=COLORS["text"], font=FONTS["label"], anchor="w",
        ).grid(row=row, column=col, sticky="w", padx=padx, pady=(8, 2))

        if field_type == "combo":
            var = tk.StringVar(value=extra[0] if extra else "")
            combo = ttk.Combobox(
                parent, textvariable=var, values=extra,
                font=FONTS["entry"], state="readonly",
            )
            combo.grid(row=row + 1, column=col, sticky="ew", padx=padx, pady=(0, 4))
            self.entries[key] = var
        else:
            show = "*" if field_type == "password" else ""
            entry = tk.Entry(
                parent, font=FONTS["entry"], relief="solid",
                bd=1, show=show, highlightthickness=0,
            )
            if extra:
                entry.insert(0, extra)
                entry.config(fg=COLORS["text_light"])
                entry.bind("<FocusIn>", lambda e, w=entry, ph=extra: self._clear_placeholder(w, ph))
                entry.bind("<FocusOut>", lambda e, w=entry, ph=extra: self._restore_placeholder(w, ph))
            entry.grid(row=row + 1, column=col, sticky="ew", padx=padx, pady=(0, 4))
            self.entries[key] = entry

    def _clear_placeholder(self, widget, placeholder):
        if widget.get() == placeholder:
            widget.delete(0, "end")
            widget.config(fg=COLORS["text"])

    def _restore_placeholder(self, widget, placeholder):
        if not widget.get():
            widget.insert(0, placeholder)
            widget.config(fg=COLORS["text_light"])

    def _build_buttons(self):
        bar = tk.Frame(self, bg=COLORS["bg"])
        bar.pack(fill="x", padx=24, pady=(0, 16))

        btn_frame = tk.Frame(bar, bg=COLORS["bg"])
        btn_frame.pack(side="right")

        cancel_btn = tk.Button(
            btn_frame, text="Cancelar", font=FONTS["button"],
            bg=COLORS["button_cancel_bg"], fg=COLORS["button_cancel_fg"],
            relief="solid", bd=1, padx=16, pady=6, cursor="hand2",
            command=self.on_cancel if self.on_cancel else lambda: None,
        )
        cancel_btn.pack(side="left", padx=(0, 8))

        submit_btn = tk.Button(
            btn_frame, text="Criar conta", font=FONTS["button"],
            bg=COLORS["primary"], fg=COLORS["white"],
            activebackground=COLORS["primary_dark"], activeforeground=COLORS["white"],
            relief="flat", bd=0, padx=16, pady=6, cursor="hand2",
            command=self._handle_submit,
        )
        submit_btn.pack(side="left")

    def _handle_submit(self):
        data = self.get_form_data()
        if self.on_submit:
            self.on_submit(data)

    def get_form_data(self) -> dict:
        data = {}
        for key, widget in self.entries.items():
            if isinstance(widget, tk.StringVar):
                data[key] = widget.get()
            else:
                value = widget.get()
                placeholder_map = {"email": "usado no login", "age": "ex.: 25"}
                if value == placeholder_map.get(key, ""):
                    value = ""
                data[key] = value
        return data

    def show_error(self, message: str):
        messagebox.showerror("Erro", message)

    def show_success(self, message: str):
        messagebox.showinfo("Sucesso", message)
