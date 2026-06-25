COLORS = {
    "primary": "#1B6B2A",
    "primary_dark": "#145220",
    "primary_light": "#6BAF7A",
    "bg": "#C5CCBB",
    "white": "#FFFFFF",
    "text": "#333333",
    "text_light": "#888888",
    "border": "#CCCCCC",
    "error": "#CC0000",
    "button_cancel_bg": "#FFFFFF",
    "button_cancel_fg": "#333333",
    "row_odd": "#EDF5ED",     # linha ímpar de tabela: verde bem claro
    "info_bg": "#F0F5F0",     # fundo da barra informativa em todas as telas
    "off_diet_bg": "#FDECEA", # fundo vermelho claro para refeições OFF_DIET
    "on_diet_fg": "#1B6B2A",  # texto verde para status ON_DIET
    "off_diet_fg": "#CC0000", # texto vermelho para status OFF_DIET
}

FONTS = {
    "title": ("Segoe UI", 16, "bold"),
    "header": ("Segoe UI", 12, "bold"),
    "header_nav": ("Segoe UI", 10),
    "label": ("Segoe UI", 10),
    "label_bold": ("Segoe UI", 10, "bold"),
    "entry": ("Segoe UI", 11),
    "button": ("Segoe UI", 10, "bold"),
    "small": ("Segoe UI", 9),
    "small_bold": ("Segoe UI", 9, "bold"),
}

ACTIVITY_FACTORS = [
    ("Sedentário (×1.2)", 1.2),
    ("Levemente ativo (×1.375)", 1.375),
    ("Moderadamente ativo (×1.55)", 1.55),
    ("Muito ativo (×1.725)", 1.725),
    ("Extremamente ativo (×1.9)", 1.9),
]

GOAL_OPTIONS = [
    ("LOSE_WEIGHT — Perda de peso", "LOSE_WEIGHT"),
    ("MAINTAIN_WEIGHT — Manutenção", "MAINTAIN_WEIGHT"),
    ("GAIN_WEIGHT — Ganho de peso", "GAIN_WEIGHT"),
]

SEX_OPTIONS = [
    ("Masculino", "MALE"),
    ("Feminino", "FEMALE"),
]

MEAL_CATEGORY_OPTIONS = [
    ("BREAKFAST — Café da manhã", "BREAKFAST"),
    ("LUNCH — Almoço", "LUNCH"),
    ("DINNER — Jantar", "DINNER"),
    ("SNACK — Lanche", "SNACK"),
]

DIET_STATUS_OPTIONS = [
    ("ON_DIET — Dentro da dieta", "ON_DIET"),
    ("OFF_DIET — Fora da dieta", "OFF_DIET"),
]
