import tkinter as tk
from datetime import datetime

from mvc.ui_constants import COLORS, FONTS

# Nomes dos dias da semana em português, começando pela segunda (índice 0 do Python)
_WEEKDAYS_PT = [
    "Segunda-feira", "Terça-feira", "Quarta-feira",
    "Quinta-feira", "Sexta-feira", "Sábado", "Domingo",
]

# Cada item da grade: (texto do botão, chave de seção enviada ao controller)
# A chave identifica qual funcionalidade foi clicada sem depender do texto exibido
_NAV_ITEMS = [
    ("Refeições",   "meals"),
    ("Lembretes",   "reminders"),
    ("Atividades",  "activities"),
    ("Calorias",    "calories"),
    ("Relatório",   "report"),
    ("Minha Conta", "account"),
]


class HomeView(tk.Frame):

    def __init__(self, master, user, on_navigate=None, on_logout=None):
        super().__init__(master, bg=COLORS["bg"])
        # Usuário logado — usado para exibir o nome na saudação
        self.user = user
        # Callback chamado ao clicar em qualquer botão da grade: recebe a chave da seção
        self.on_navigate = on_navigate
        # Callback chamado ao clicar em "Sair" — normalmente volta para a tela de login
        self.on_logout = on_logout
        self._build_header()
        self._build_body()

    def _build_header(self):
        # Barra superior verde, igual às outras telas do app
        header = tk.Frame(self, bg=COLORS["primary"], height=45)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Nome do app à esquerda
        tk.Label(
            header, text="DietTracker",
            fg=COLORS["white"], bg=COLORS["primary"], font=FONTS["header"],
        ).pack(side="left", padx=16)

        # Título da tela centralizado usando place (não interfere nos itens laterais)
        tk.Label(
            header, text="Painel Principal",
            fg=COLORS["white"], bg=COLORS["primary"], font=FONTS["header_nav"],
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Botão "Sair" à direita — dispara o callback de logout ao clicar
        sair = tk.Label(
            header, text="Sair",
            fg=COLORS["white"], bg=COLORS["primary"], font=FONTS["header_nav"], cursor="hand2",
        )
        sair.pack(side="right", padx=16)
        sair.bind("<Button-1>", lambda e: self.on_logout() if self.on_logout else None)

        # Botão "Conta" à direita do "Sair" — navega para a seção de perfil
        conta = tk.Label(
            header, text="Conta",
            fg=COLORS["white"], bg=COLORS["primary"], font=FONTS["header_nav"], cursor="hand2",
        )
        conta.pack(side="right")
        conta.bind("<Button-1>", lambda e: self._navigate("account"))

    def _build_body(self):
        # Frame externo com a cor de fundo da tela, cria o espaçamento lateral
        outer = tk.Frame(self, bg=COLORS["bg"])
        outer.pack(fill="both", expand=True, padx=24, pady=(16, 16))

        # Card branco que contém todo o conteúdo principal
        card = tk.Frame(outer, bg=COLORS["white"])
        card.pack(fill="both", expand=True)

        # Área interna do card com padding
        inner = tk.Frame(card, bg=COLORS["white"])
        inner.pack(fill="both", expand=True, padx=28, pady=20)

        # --- Linha de saudação ---
        # Frame auxiliar para colocar nome e data lado a lado (left e right)
        greeting_row = tk.Frame(inner, bg=COLORS["white"])
        greeting_row.pack(fill="x", pady=(0, 16))

        # Exibe só o primeiro nome para não ocupar muito espaço
        first_name = self.user.name.split()[0]
        tk.Label(
            greeting_row, text=f"Olá, {first_name}!",
            bg=COLORS["white"], fg=COLORS["text"], font=FONTS["title"],
        ).pack(side="left")

        # Data atual formatada em português, alinhada à direita
        tk.Label(
            greeting_row, text=self._current_date_pt(),
            bg=COLORS["white"], fg=COLORS["text_light"], font=FONTS["small"],
        ).pack(side="right", anchor="s")

        # --- Grade de navegação (2 linhas × 3 colunas) ---
        grid = tk.Frame(inner, bg=COLORS["white"])
        grid.pack(fill="both", expand=True)

        # Cria cada botão e posiciona na célula certa da grade
        for i, (label, section) in enumerate(_NAV_ITEMS):
            row, col = divmod(i, 3)  # divmod(0,3)=(0,0), divmod(1,3)=(0,1), etc.
            btn = self._nav_button(grid, label, section)
            btn.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

        # Faz as 3 colunas crescerem igualmente quando a janela for redimensionada
        for col in range(3):
            grid.columnconfigure(col, weight=1)
        # Faz as 2 linhas crescerem igualmente
        for row in range(2):
            grid.rowconfigure(row, weight=1)

        # --- Barra informativa ---
        # Frame que agrupa a faixa verde lateral e o texto de aviso
        info_bar = tk.Frame(inner, bg=COLORS["white"])
        info_bar.pack(fill="x", pady=(12, 0))

        # Faixa verde fina à esquerda — detalhe visual do design system
        tk.Frame(info_bar, bg=COLORS["primary"], width=4).pack(side="left", fill="y")

        # Texto da mensagem com fundo levemente esverdeado
        tk.Label(
            info_bar,
            text="  Bem-vindo(a)! Use o menu acima para navegar entre as funcionalidades.",
            bg=COLORS["info_bg"], fg=COLORS["text"], font=FONTS["small"], anchor="w",
        ).pack(side="left", fill="x", expand=True, ipady=8)

    def _nav_button(self, parent, label: str, section: str) -> tk.Frame:
        # Cada botão é um Frame com borda verde (cor primária do design system)
        # Usamos Frame + Label em vez de tk.Button para ter controle total do visual
        frame = tk.Frame(
            parent, bg=COLORS["white"],
            relief="solid", bd=1,
            highlightthickness=1,
            highlightbackground=COLORS["primary_light"],
            cursor="hand2",
        )

        # Texto centralizado dentro do botão
        lbl = tk.Label(
            frame, text=label,
            bg=COLORS["white"], fg=COLORS["text"], font=FONTS["button"], anchor="center",
        )
        lbl.pack(expand=True, pady=20)

        # O clique precisa ser registrado tanto no frame quanto no label interno,
        # pois o label fica por cima e pode "bloquear" o evento do frame
        for widget in (frame, lbl):
            widget.bind("<Button-1>", lambda e, s=section: self._navigate(s))

        return frame

    def _navigate(self, section: str):
        # Repassa a seção escolhida ao controller via callback
        if self.on_navigate:
            self.on_navigate(section)

    @staticmethod
    def _current_date_pt() -> str:
        # Formata a data atual como "Segunda-feira, 20/04/2026"
        now = datetime.now()
        return f"{_WEEKDAYS_PT[now.weekday()]}, {now.strftime('%d/%m/%Y')}"
