import tkinter as tk
from datetime import date as date_type
from tkinter import messagebox
from typing import Literal

from mvc.models.diet_status import DietStatus
from mvc.ui_constants import COLORS, FONTS

# Atalhos locais para as cores de linha — valores vêm do design system (ui_constants)
_ROW_EVEN = COLORS["white"]
_ROW_ODD = COLORS["row_odd"]

_Anchor = Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]

# Colunas de dados: (cabeçalho exibido, atributo do objeto, alinhamento do texto)
# A coluna de ações (Editar/Excluir) é adicionada separadamente em _build_data_row
_COLUMNS: list[tuple[str, str, _Anchor]] = [
    ("Horário", "time", "w"),
    ("Categoria", "category", "w"),
    ("Nome", "name", "w"),
    ("Calorias ▼", "calories", "w"),
    ("Status", "status", "center"),
]


class MealsListView(tk.Frame):
    def __init__(
        self,
        master,
        on_back=None,
        on_new=None,
        on_edit=None,
        on_delete=None,
        on_date_change=None,
    ):
        super().__init__(master, bg=COLORS["bg"])
        # Callbacks configurados pelo NavigationController após a criação da view
        self.on_back = on_back          # "← Voltar" — volta ao painel principal
        self.on_new = on_new            # "+ Nova refeição" — abre o formulário vazio
        self.on_edit = on_edit          # chamado com a refeição ao clicar "Editar"
        self.on_delete = on_delete      # chamado com a refeição ao clicar "Excluir"
        self.on_date_change = (
            on_date_change              # chamado quando o usuário muda a data do filtro
        )

        self._build_header()
        self._build_body()

    def _build_header(self):
        # Barra superior verde, igual ao padrão das outras telas
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
            text="Refeições",
            fg=COLORS["white"],
            bg=COLORS["primary"],
            font=FONTS["header_nav"],
        ).place(relx=0.5, rely=0.5, anchor="center")

        # "← Voltar" dispara o callback de retorno ao painel principal
        back = tk.Label(
            header,
            text="← Voltar",
            fg=COLORS["white"],
            bg=COLORS["primary"],
            font=FONTS["header_nav"],
            cursor="hand2",
        )
        back.pack(side="right", padx=16)
        back.bind("<Button-1>", lambda e: self.on_back() if self.on_back else None)

    def _build_body(self):
        outer = tk.Frame(self, bg=COLORS["bg"])
        outer.pack(fill="both", expand=True, padx=24, pady=(16, 16))

        card = tk.Frame(outer, bg=COLORS["white"])
        card.pack(fill="both", expand=True)

        inner = tk.Frame(card, bg=COLORS["white"])
        inner.pack(fill="both", expand=True, padx=28, pady=20)

        # --- Linha de título com filtro de data e botão de nova refeição ---
        title_row = tk.Frame(inner, bg=COLORS["white"])
        title_row.pack(fill="x", pady=(0, 12))

        tk.Label(
            title_row,
            text="Minhas refeições",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONTS["label_bold"],
        ).pack(side="left")

        # Botão "+ Nova refeição" alinhado à direita
        tk.Button(
            title_row,
            text="+ Nova refeição",
            font=FONTS["button"],
            bg=COLORS["primary"],
            fg=COLORS["white"],
            activebackground=COLORS["primary_dark"],
            activeforeground=COLORS["white"],
            relief="flat",
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=lambda: self.on_new() if self.on_new else None,
        ).pack(side="right")

        # Campo de data para filtrar as refeições exibidas
        # O usuário digita a data e pressiona Enter ou sai do campo para filtrar
        self._date_entry = tk.Entry(
            title_row,
            font=FONTS["entry"],
            relief="solid",
            bd=1,
            width=12,
            highlightthickness=0,
        )
        self._date_entry.insert(0, date_type.today().strftime("%d/%m/%Y"))
        self._date_entry.pack(side="right", padx=(0, 16))
        self._date_entry.bind("<FocusOut>", lambda e: self._handle_date_change())
        self._date_entry.bind("<Return>", lambda e: self._handle_date_change())

        tk.Label(
            title_row,
            text="Data:",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONTS["label"],
        ).pack(side="right", padx=(12, 4))

        # --- Tabela de refeições ---
        # Frame único para cabeçalho + dados usando grid.
        # Ao usar um único grid para todas as linhas, o tkinter calcula a largura
        # de cada coluna com base no conteúdo mais largo, garantindo alinhamento perfeito.
        self._table = tk.Frame(inner, bg=COLORS["white"])
        self._table.pack(fill="x")

        # Configuração das colunas: Horário, Categoria, Nome (mais espaço), Calorias, Status, Ações
        self._table.columnconfigure(0, weight=1)  # Horário
        self._table.columnconfigure(1, weight=2)  # Categoria
        self._table.columnconfigure(2, weight=3)  # Nome
        self._table.columnconfigure(3, weight=1)  # Calorias
        self._table.columnconfigure(4, weight=1)  # Status
        self._table.columnconfigure(5, weight=0)  # Ações

        # Linha 0 é o cabeçalho fixo — nunca será destruída no reload
        self._build_table_header()

        # --- Barra de total de calorias ---
        info_bar = tk.Frame(inner, bg=COLORS["white"])
        info_bar.pack(fill="x", pady=(8, 0))

        # Label atualizado pelo método load_meals com o total calculado
        self._total_label = tk.Label(
            info_bar,
            text="Total do dia: 0 kcal",
            bg=COLORS["white"],
            fg=COLORS["text"],
            font=FONTS["label_bold"],
            anchor="e",
        )
        self._total_label.pack(side="right")

    def _build_table_header(self):
        # Linha 0 do grid: células do cabeçalho com fundo verde para as colunas de dados
        # sticky="ew" faz cada célula preencher toda a largura da sua coluna
        for col, (title, _, anchor) in enumerate(_COLUMNS):
            tk.Label(
                self._table,
                text=title,
                bg=COLORS["primary"],
                fg=COLORS["white"],
                font=FONTS["small_bold"],
                anchor=anchor,
                padx=4,
                pady=6,
            ).grid(row=0, column=col, sticky="ew")

        # Cabeçalho da coluna de ações — centralizado pois os botões ficam no meio da célula
        tk.Label(
            self._table,
            text="Ações",
            bg=COLORS["primary"],
            fg=COLORS["white"],
            font=FONTS["small_bold"],
            anchor="center",
            padx=4,
            pady=6,
        ).grid(row=0, column=5, sticky="ew")

    def load_meals(self, meals: list, total_calories: float):
        # Remove apenas as linhas de dados antigas (linha 0 = cabeçalho, permanece intacta)
        # Destrói todos os widgets do grid que estão nas linhas 1 em diante
        for widget in self._table.winfo_children():
            if not isinstance(widget, tk.Widget):
                continue
            info = widget.grid_info()
            if info and int(info["row"]) > 0:
                widget.destroy()

        # Cria uma linha de dados para cada refeição, com cores alternadas
        for i, meal in enumerate(meals):
            # OFF_DIET recebe fundo vermelho claro; demais alternam branco/verde claro
            if meal.status == DietStatus.OFF_DIET:
                bg = COLORS["off_diet_bg"]
            else:
                bg = _ROW_EVEN if i % 2 == 0 else _ROW_ODD
            self._build_data_row(i, meal, bg)

        # Atualiza o texto do total de calorias com o valor calculado pelo controller
        self._total_label.config(text=f"Total do dia: {total_calories:,.0f} kcal".replace(",", "."))

    def _build_data_row(self, idx: int, meal, bg: str):
        # Formata os valores de cada coluna para exibição
        time_str = meal.time.strftime("%H:%M") if meal.time else ""
        category_str = meal.category.value if meal.category else ""
        status_str = meal.status.value if meal.status else ""

        # Cor do texto do status: verde para ON_DIET, vermelho para OFF_DIET
        if meal.status == DietStatus.ON_DIET:
            status_fg = COLORS["on_diet_fg"]
        elif meal.status == DietStatus.OFF_DIET:
            status_fg = COLORS["off_diet_fg"]
        else:
            status_fg = COLORS["text"]

        values = [
            time_str,
            category_str,
            meal.name,
            f"{meal.calories:.0f}" if meal.calories else "0",
        ]

        # Cria um Label por coluna de dado na linha idx+1 (linha 0 é o cabeçalho)
        for col, (value, (_, _, anchor)) in enumerate(zip(values, _COLUMNS[:4])):
            tk.Label(
                self._table,
                text=value,
                bg=bg,
                fg=COLORS["text"],
                font=FONTS["small"],
                anchor=anchor,
                padx=4,
                pady=6,
            ).grid(row=idx + 1, column=col, sticky="ew")

        # Coluna de status com cor diferenciada
        tk.Label(
            self._table,
            text=status_str,
            bg=bg,
            fg=status_fg,
            font=FONTS["small_bold"],
            anchor="center",
            padx=4,
            pady=6,
        ).grid(row=idx + 1, column=4, sticky="ew")

        # Coluna de ações: frame que herda a cor da linha para manter as listras
        btn_frame = tk.Frame(self._table, bg=bg)
        btn_frame.grid(row=idx + 1, column=5, sticky="nsew")

        # "Editar" como link na cor primária do design system
        edit_lbl = tk.Label(
            btn_frame,
            text="Editar",
            bg=bg,
            fg=COLORS["primary"],
            font=FONTS["small"],
            cursor="hand2",
        )
        edit_lbl.pack(side="left", padx=(4, 0), pady=6)
        edit_lbl.bind(
            "<Button-1>",
            lambda e, m=meal: self.on_edit(m) if self.on_edit else None,
        )

        # Separador visual entre os dois links
        tk.Label(
            btn_frame,
            text=" | ",
            bg=bg,
            fg=COLORS["border"],
            font=FONTS["small"],
        ).pack(side="left", pady=6)

        # "Excluir" como link na cor de erro (vermelho)
        del_lbl = tk.Label(
            btn_frame,
            text="Excluir",
            bg=bg,
            fg=COLORS["error"],
            font=FONTS["small"],
            cursor="hand2",
        )
        del_lbl.pack(side="left", padx=(0, 4), pady=6)
        del_lbl.bind(
            "<Button-1>",
            lambda e, m=meal: self.on_delete(m) if self.on_delete else None,
        )

    def get_date_str(self) -> str:
        return self._date_entry.get().strip()

    def _handle_date_change(self):
        if self.on_date_change:
            self.on_date_change(self._date_entry.get().strip())

    def show_error(self, message: str):
        messagebox.showerror("Erro", message)

    def show_confirm(self, message: str) -> bool:
        return messagebox.askyesno("Confirmar", message)
