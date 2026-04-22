import tkinter as tk
from mvc.models import init_db
from mvc.ui_constants import COLORS
from mvc.controllers.navigation_controller import NavigationController

if __name__ == "__main__":
    root = tk.Tk()
    root.title("DietTracker")
    root.configure(bg=COLORS["bg"])
    root.geometry("660x520")
    root.resizable(False, False)

    init_db()

    nav = NavigationController(root)
    nav.show_login()

    root.mainloop()
