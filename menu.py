import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
from database.models import fetch_books


class MenuBar:
    """Crea la barra de menú para la aplicación."""

    @staticmethod
    def add_menu(root, main_frame):
        barra = tk.Menu(root)
        root.config(menu=barra)

        # Menús principales
        menu_inicio = tk.Menu(barra, tearoff=0)
        menu_ventas = tk.Menu(barra, tearoff=0)
        menu_consultas = tk.Menu(barra, tearoff=0)
        menu_gestion = tk.Menu(barra, tearoff=0)
        menu_acerca = tk.Menu(barra, tearoff=0)


        # Agregar menús a la barra
        barra.add_cascade(label='Inicio', menu=menu_inicio)
        barra.add_cascade(label='Ventas', menu=menu_ventas)
        barra.add_cascade(label='Consultas', menu=menu_consultas)
        barra.add_cascade(label="Gestión", menu=menu_gestion)
        barra.add_cascade(label='Acerca de..', menu=menu_acerca)

        # Opciones del menú Inicio
        menu_inicio.add_command(label='Salir', command=root.destroy)

        # Opciones del menú Ventas
        menu_ventas.add_command(
            label="Gestionar Ventas",
            command=main_frame.show_sales_view
        )

        # Opciones del menú Consultas
        menu_consultas.add_command(
            label="Agregar Libro",
            command=lambda: main_frame.show_form(),
            accelerator="Ctrl+N"
        )
        menu_consultas.add_command(
            label="Editar Libro",
            command=lambda: main_frame.show_edit_view(),
            accelerator="Ctrl+E"
        )
        menu_consultas.add_separator()
        menu_consultas.add_command(
            label="Lista de Libros",
            command=lambda: open_book_list(root),
            accelerator="Ctrl+L"
        )

        # Opciones del menú Gestión
        menu_gestion.add_command(label="Libros", command=main_frame.show_books)
        menu_gestion.add_command(label="Autores", command=main_frame.show_authors)

        # Opciones del menú Acerca de
        menu_acerca.add_command(label='Sobre la Librería', command=MenuBar.show_about)
        menu_acerca.add_command(label='Repositorio', command=MenuBar.open_repository)

        # Configurar accesos rápidos (hotkeys)
        root.bind_all("<Control-n>", lambda event: main_frame.show_form())
        root.bind_all("<Control-e>", lambda event: main_frame.show_edit_view())
        root.bind_all("<Control-l>", lambda event: open_book_list(root))

    @staticmethod
    def show_about():
        """Muestra información sobre la aplicación."""
        about_message = (
            "Gestión de Librería\n"
            "Versión: 1.0\n"
            "------------------------\n"
            "Desarrollado por:\n"
            "Jorge Gabriel Molina\n"
            "\n"
            "Curso: Python Intermedio 2024\n"
            "Institución: Municipalidad de Tres de Febrero\n"
            "------------------------\n"
            "¡Gracias por la oportunidad!"
        )
        messagebox.showinfo("Sobre la Librería", about_message)

    @staticmethod
    def open_repository():
        """Abre una ventana o muestra información sobre el repositorio."""
        messagebox.showinfo(
            "Repositorio",
            "Repositorio en GitHub: https://github.com/Jgmdevelopers/Libreria_3F"
        )

    @staticmethod
    def open_help():
        """Muestra información de ayuda."""
        messagebox.showinfo(
            "Ayuda",
            "Para soporte, contacta a soporte@tulibreria.com\nO visita nuestra página de ayuda."
        )


def open_book_list(root):
    """Abre una ventana para listar libros."""
    if hasattr(root, "book_list_window") and root.book_list_window.winfo_exists():
        root.book_list_window.lift()
        return

    root.book_list_window = Toplevel(root)
    root.book_list_window.title("Lista de Libros")
    root.book_list_window.geometry("600x400")

    table = ttk.Treeview(
        root.book_list_window,
        columns=("ID", "Título", "Autor", "Género", "ISBN", "Precio", "Stock")
    )
    table.heading("#0", text="")
    table.heading("ID", text="ID")
    table.heading("Título", text="Título")
    table.heading("Autor", text="Autor")
    table.heading("Género", text="Género")
    table.heading("ISBN", text="ISBN")
    table.heading("Precio", text="Precio")
    table.heading("Stock", text="Stock")
    table.column("#0", width=0, stretch=tk.NO)

    # Poblar la tabla con datos
    for book in fetch_books():
        table.insert("", "end", values=book)

    table.pack(fill=tk.BOTH, expand=True)

def show_sales_view(self):
    """Muestra la vista de ventas."""
    self.clear_views()
    self.sales_view.pack(fill=tk.BOTH, expand=True)
