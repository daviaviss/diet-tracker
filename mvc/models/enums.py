import enum


class NutritionalGoal(enum.Enum):
    LOSE_WEIGHT = "LOSE_WEIGHT"
    MAINTAIN_WEIGHT = "MAINTAIN_WEIGHT"
    GAIN_WEIGHT = "GAIN_WEIGHT"


class MealCategory(enum.Enum):
    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"
    SNACK = "SNACK"


class DietStatus(enum.Enum):
    ON_DIET = "ON_DIET"
    OFF_DIET = "OFF_DIET"
