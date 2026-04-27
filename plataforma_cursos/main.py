"""
Punto de entrada principal del Sistema E-Learning.
Ejecuta este archivo para iniciar la aplicación.
"""

import tkinter as tk
from gui import SistemaELearningGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaELearningGUI(root)
    root.mainloop()