from database.connection import create_tables
from form import MainFrame
from menu import MenuBar
import tkinter as tk
import logging

def main():
    # Configuración del logger
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    create_tables()  # Crear las tablas al iniciar
    ventana = tk.Tk()
    ventana.geometry("1000x600")
    ventana.resizable(False, False)

    # Crear el marco principal
    main_frame = MainFrame(ventana)

    # Agregar el menú
    MenuBar.add_menu(ventana, main_frame)
    main_frame.show_edit_view()
    ventana.mainloop()

if __name__ == "__main__":
    main()
