import os
import tkinter as tk
import logging

from tkinter import ttk, messagebox, filedialog
from database.models import insert_book, update_book, fetch_books, search_books, delete_book, fetch_authors, \
    get_author_by_name, insert_author, fetch_sales, fetch_sales_report, insert_sale
import csv

class MainFrame(tk.Frame):
    """Marco principal que gestiona las diferentes vistas."""

    def __init__(self, root=None):
        super().__init__(root, bg="#F7F7F7")
        self.root = root
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        logging.debug("[DEBUG] Inicializando MainFrame.")
        # Encabezado
        header = tk.Frame(self, bg="#2C3E50", height=60)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="Gestión de Librería",
            font=("Helvetica", 24, "bold"),
            bg="#2C3E50",
            fg="white"
        )
        title.pack(pady=15)

        # Estilo global para los botones
        style = ttk.Style()
        style.configure("TEntry", padding=5, borderwidth=2, relief="solid")
        style.configure("TButton", font=("Helvetica", 12), padding=5)
        style.map("TButton", background=[("active", "#3498DB")])



        # Crear las vistas
        self.form_view = BookForm(self)
        self.edit_view = EditView(self)
        self.author_form = AuthorForm(self)
        self.sales_view = SalesView(self)  # Instancia la vista de ventas


        # Mostrar la vista inicial
        self.show_form()

    def show_sales_view(self):
        """Muestra la vista de gestión de ventas."""
        self.clear_views()  # Oculta otras vistas
        self.sales_view.pack(fill=tk.BOTH, expand=True)  # Muestra la vista de ventas

    def show_books(self):

        self.clear_views()
        self.form_view.pack(fill=tk.BOTH, expand=True)

    def show_authors(self):
        """Muestra la vista de gestión de autores."""
        self.clear_views()
        self.author_form.pack(fill=tk.BOTH, expand=True)

    def clear_views(self):
        """Oculta todas las vistas."""
        self.form_view.pack_forget()
        self.edit_view.pack_forget()
        self.author_form.pack_forget()
        self.sales_view.pack_forget()

    def show_form(self):
        """Muestra el formulario para agregar o editar libros."""
        self.clear_views()  # Ocultar otras vistas

        if self.form_view.book_id is None:  # Solo limpiar si no es edición
            self.form_view.clear_fields()

        self.form_view.pack(fill=tk.BOTH, expand=True)

    def show_edit_view(self):
        """Muestra la vista de edición."""
        logging.debug("[DEBUG] Ejecutando show_edit_view() en MainFrame.")
        self.clear_views()
        self.edit_view.load_books()
        self.edit_view.pack(fill=tk.BOTH, expand=True)




class BookForm(tk.Frame):
    """Formulario para la gestión de libros (crear/editar)."""

    def __init__(self, root=None):
        super().__init__(root, bg="#E8F0FE")  # Fondo suave
        self.root = root

        self.entries = {}
        self.book_id = None  # Almacena el ID del libro para edición
        self.create_widgets()
        self.disable_fields()  # Deshabilitar los campos al iniciar

    def create_widgets(self):
        """Crea el diseño completo del formulario."""
        # Título del formulario
        title = tk.Label(
            self,
            text="Formulario de Registro de Libros",
            font=("Helvetica", 18, "bold"),
            bg="#E8F0FE",
            fg="#1C5D8B"
        )
        title.pack(pady=20)

        # Contenedor del formulario
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Crear las etiquetas y entradas
        self.create_labels_and_inputs(form_frame)

        # Botones principales
        self.create_buttons()

    def create_labels_and_inputs(self, parent):
        """Crea etiquetas y campos de entrada."""
        labels = ["Título:", "Autor:", "Género:", "ISBN:", "Precio:", "Stock:"]
        input_types = [
            tk.Entry,
            tk.Entry,
            lambda parent: ttk.Combobox(parent, values=["Ficción", "No Ficción", "Educativo", "Ciencia"],
                                        state="readonly"),
            tk.Entry,
            tk.Entry,
            tk.Entry,
        ]

        for idx, (label_text, input_type) in enumerate(zip(labels, input_types)):
            # Usa el estilo configurado para las etiquetas
            label = ttk.Label(parent, text=label_text, style="Custom.TLabel")
            label.grid(row=idx, column=0, sticky="e", padx=10, pady=5)

            input_widget = input_type(parent)
            input_widget.grid(row=idx, column=1, padx=10, pady=5, sticky="ew")

            # Almacenar la entrada para referencia futura
            self.entries[label_text.strip(":")] = input_widget

        parent.columnconfigure(1, weight=1)

    def create_buttons(self):
        """Crea los botones principales."""
        button_frame = tk.Frame(self, bg="#E8F0FE")
        button_frame.pack(pady=10)

        # Botón Nuevo
        self.btn_new = tk.Button(
            button_frame,
            text="Nuevo",
            command=self.enable_fields,
            font=("Helvetica", 12, "bold"),
            bg="#1C5D8B",
            fg="#FFFFFF",
            width=15,
            cursor="hand2",
            activebackground="#3F80BF",
            activeforeground="#FFFFFF"
        )
        self.btn_new.grid(row=0, column=0, padx=10, pady=10)

        # Botón Guardar
        self.btn_save = tk.Button(
            button_frame,
            text="Guardar",
            command=self.save_record,
            state="disabled",
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="#FFFFFF",
            width=15,
            cursor="hand2",
            activebackground="#45A049",
            activeforeground="#FFFFFF"
        )
        self.btn_save.grid(row=0, column=1, padx=10, pady=10)

        # Botón Cancelar
        self.btn_cancel = tk.Button(
            button_frame,
            text="Cancelar",
            command=self.disable_fields,
            state="disabled",
            font=("Helvetica", 12, "bold"),
            bg="#A90A0A",
            fg="#FFFFFF",
            width=15,
            cursor="hand2",
            activebackground="#BF3535",
            activeforeground="#FFFFFF"
        )
        self.btn_cancel.grid(row=0, column=2, padx=10, pady=10)

    def enable_fields(self):
            """Habilita los campos del formulario."""
            for entry in self.entries.values():
                entry.config(state="normal")
            self.btn_save.config(state="normal")
            self.btn_cancel.config(state="normal")
            self.btn_new.config(state="disabled")

    def disable_fields(self):
        """Deshabilita los campos del formulario y limpia los valores."""
        # Limpiar los valores de los campos

        self.clear_fields()

        # Deshabilitar los campos de entrada
        for entry in self.entries.values():
            entry.config(state="disabled")  # Deshabilita los campos


        # Deshabilitar los botones de Guardar y Cancelar
        self.btn_save.config(state="disabled")  # Botón Guardar
        self.btn_cancel.config(state="disabled")  # Botón Cancelar

        # Habilitar el botón Nuevo
        self.btn_new.config(state="normal")  # Botón Nuevo

        # Forzar actualización de la interfaz
        self.update()

    def clear_fields(self):
        """Limpia los valores de todos los campos del formulario."""

        for field_name, entry in self.entries.items():
            if isinstance(entry, ttk.Combobox):
                entry.set('')  # Limpia el valor del Combobox

            elif isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)  # Limpia el valor del Entry

        self.book_id = None  # Resetea el ID del libro
        self.update()  # Forzar actualización de la interfaz

    def save_record(self):
        """Guarda o actualiza el registro del libro en la base de datos."""
        try:
            # Validar campos requeridos
            required_fields = ["Título", "Autor", "Género", "ISBN", "Precio", "Stock"]
            missing_fields = [field for field in required_fields if not self.entries[field].get().strip()]

            if missing_fields:
                messagebox.showerror(
                    "Error al guardar",
                    f"Por favor completa los siguientes campos: {', '.join(missing_fields)}"
                )
                return  # Salir si faltan campos

            # Preparar los datos
            titulo = self.entries["Título"].get().strip()
            autor = self.entries["Autor"].get().strip()
            genero = self.entries["Género"].get().strip()
            isbn = self.entries["ISBN"].get().strip()
            precio = float(self.entries["Precio"].get().strip())
            stock = int(self.entries["Stock"].get().strip())

            # Crear los datos del libro para enviar al modelo
            book_data = (titulo, autor, genero, isbn, precio, stock)

            print(f"[DEBUG] Datos enviados a insert_book: {book_data}")

            if self.book_id is None:
                # Insertar un nuevo libro
                insert_book(book_data)  # El modelo se encarga de todo
                messagebox.showinfo("Éxito", "Libro guardado correctamente.")
            else:
                # Actualizar un libro existente
                update_data = (*book_data, self.book_id)
                update_book(self.book_id, update_data)
                messagebox.showinfo("Éxito", "Libro actualizado correctamente.")

            # Limpiar y actualizar la interfaz
            self.clear_fields()
            self.disable_fields()
            self.root.edit_view.load_books()  # Actualizar lista de libros
            self.root.author_form.load_authors()  # Actualizar lista de autores

        except ValueError as ve:
            messagebox.showerror("Error de validación", "Los campos 'Precio' y 'Stock' deben ser valores numéricos.")
            print(f"[ERROR] Validación fallida: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el libro. Error: {e}")
            print(f"[ERROR] Error al guardar el libro: {e}")

    def load_book_data(self, data):
        """Carga los datos de un libro en el formulario para edición."""
        # Habilitar los campos para que los valores sean visibles
        self.enable_fields()

        fields = ["Título", "Autor", "Género", "ISBN", "Precio", "Stock"]
        for idx, field in enumerate(fields):
            self.entries[field].delete(0, tk.END)  # Limpia el campo actual
            if field == "Género":
                # Para ttk.Combobox, se usa set()
                self.entries[field].set(data[idx + 1])
            else:
                self.entries[field].insert(0, data[idx + 1])  # Inserta el valor correspondiente


        self.book_id = data[0]  # Almacenar el ID del libro para edición

class EditView(tk.Frame):
    """Vista para editar libros."""

    def __init__(self, root=None):
        super().__init__(root, bg="#F7F7F7")
        self.root = root
        self.books = []
        self.create_widgets()
        self.load_books()  # Carga los libros inicialmente

    def create_widgets(self):
        """Crea los elementos para buscar, editar y exportar libros."""
        # Título principal de la vista
        title = tk.Label(
            self,
            text="Edición y Búsqueda de Libros",  # Texto del título
            font=("Helvetica", 18, "bold"),  # Fuente estilizada
            bg="#F7F7F7",  # Fondo gris claro
            fg="#1C5D8B"  # Texto azul oscuro
        )
        title.pack(pady=20)  # Espaciado vertical del título

        # Barra de búsqueda
        search_frame = tk.Frame(self)  # Contenedor para la barra de búsqueda
        search_frame.pack(pady=10, fill=tk.X, expand=True)  # Ajusta el contenedor al ancho completo

        search_label = tk.Label(search_frame, text="Título:", font=("Arial", 12))  # Etiqueta para el campo de búsqueda
        search_label.grid(row=0, column=0, padx=10, pady=5)  # Posiciona la etiqueta

        self.search_entry = tk.Entry(search_frame, font=("Arial", 12))  # Campo de entrada para el texto de búsqueda
        self.search_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")  # Posiciona el campo de entrada

        search_button = tk.Button(
            search_frame,
            text="Buscar",  # Texto del botón
            command=self.search_books,  # Comando para buscar libros
            font=("Arial", 12, "bold"),  # Fuente estilizada
            bg="#1C5D8B",  # Fondo azul oscuro
            fg="#FFFFFF",  # Texto blanco
            cursor="hand2",  # Cambia el cursor a "mano" al pasar sobre el botón
            activebackground="#3F80BF",  # Color de fondo cuando está activo
            activeforeground="#FFFFFF"  # Color del texto cuando está activo
        )
        search_button.grid(row=0, column=2, padx=10, pady=5)  # Posiciona el botón

        search_frame.columnconfigure(1, weight=1)  # Permite que el campo de entrada se expanda horizontalmente

        # Botón para limpiar filtro
        clear_button = tk.Button(
            search_frame,
            text="Limpiar",
            command=self.clear_search,
            font=("Arial", 12, "bold"),
            bg="#F39C12",
            fg="#FFFFFF",
            cursor="hand2",
            activebackground="#F7B733",
            activeforeground="#FFFFFF"
        )
        clear_button.grid(row=0, column=3, padx=10, pady=5)


        search_frame.columnconfigure(1, weight=1)


        # Contenedor para la tabla y los scrollbars
        table_frame = tk.Frame(self)  # Contenedor de la tabla
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Ajusta el contenedor al área disponible

        # Scrollbars (barras de desplazamiento)
        x_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)  # Scroll horizontal
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)  # Posiciona el scroll en la parte inferior

        y_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)  # Scroll vertical
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)  # Posiciona el scroll en el lado derecho

        # Estilos para la tabla
        style = ttk.Style()  # Crea un estilo para personalizar la tabla
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))  # Encabezados con fuente en negrita
        style.configure("Treeview", font=("Helvetica", 10), rowheight=20)  # Fuente y altura de las filas
        style.map("Treeview", background=[("selected", "#D5F5E3")],
                  foreground=[("selected", "#34495E")])  # Colores al seleccionar filas

        # Tabla con scrollbars
        self.table = ttk.Treeview(
            table_frame,
            columns=("ID", "Título", "Autor", "Género", "ISBN", "Precio", "Stock"),  # Columnas de la tabla
            show="headings",  # Oculta la primera columna por defecto
            xscrollcommand=x_scroll.set,  # Vincula el scroll horizontal
            yscrollcommand=y_scroll.set  # Vincula el scroll vertical
        )

        # Configuración de los scrollbars
        x_scroll.config(command=self.table.xview)  # Conecta el scroll horizontal
        y_scroll.config(command=self.table.yview)  # Conecta el scroll vertical

        # Encabezados de las columnas de la tabla
        self.table.heading("ID", text="ID")
        self.table.heading("Título", text="Título")
        self.table.heading("Autor", text="Autor")
        self.table.heading("Género", text="Género")
        self.table.heading("ISBN", text="ISBN")
        self.table.heading("Precio", text="Precio")
        self.table.heading("Stock", text="Stock")

        # Configuración de las columnas de la tabla
        self.table.column("ID", width=50, anchor="center")  # Ancho y alineación del ID
        self.table.column("Título", width=200, anchor="w")  # Título alineado a la izquierda
        self.table.column("Autor", width=150, anchor="w")  # Autor alineado a la izquierda
        self.table.column("Género", width=100, anchor="center")  # Género centrado
        self.table.column("ISBN", width=150, anchor="center")  # ISBN centrado
        self.table.column("Precio", width=100, anchor="e")  # Precio alineado a la derecha
        self.table.column("Stock", width=100, anchor="e")  # Stock alineado a la derecha

        self.table.pack(fill=tk.BOTH, expand=True)  # Ajusta la tabla al área disponible

        # Evento de doble clic para editar
        self.table.bind("<Double-1>", self.load_book_for_edit)  # Vincula el doble clic con una acción

        # Botones para exportar y eliminar
        button_frame = tk.Frame(self)  # Contenedor para los botones
        button_frame.pack(pady=10)  # Espaciado vertical para los botones

        export_button = tk.Button(
            button_frame,
            text="Exportar a CSV",  # Texto del botón
            command=self.export_to_csv,  # Comando para exportar datos
            font=("Arial", 12, "bold"),  # Fuente estilizada
            bg="#4CAF50",  # Fondo verde
            fg="#FFFFFF",  # Texto blanco
            cursor="hand2",  # Cambia el cursor a "mano" al pasar sobre el botón
            activebackground="#45A049",  # Fondo activo
            activeforeground="#FFFFFF"  # Texto activo
        )
        export_button.grid(row=0, column=1, padx=10, pady=5)  # Posiciona el botón

        delete_button = tk.Button(
            button_frame,
            text="Eliminar",  # Texto del botón
            command=self.delete_selected_book,  # Comando para eliminar un libro
            font=("Arial", 12, "bold"),  # Fuente estilizada
            bg="#A90A0A",  # Fondo rojo
            fg="#FFFFFF",  # Texto blanco
            cursor="hand2",  # Cambia el cursor a "mano"
            activebackground="#BF3535",  # Fondo activo
            activeforeground="#FFFFFF"  # Texto activo
        )
        delete_button.grid(row=0, column=2, padx=10, pady=5)  # Posiciona el botón

        preview_button = tk.Button(
            button_frame,
            text="Vista Previa",  # Texto del botón
            command=self.preview_books,  # Comando para la vista previa
            font=("Arial", 12, "bold"),  # Fuente estilizada
            bg="#F39C12",  # Fondo naranja
            fg="#FFFFFF",  # Texto blanco
            cursor="hand2",  # Cambia el cursor a "mano" al pasar sobre el botón
            activebackground="#F7B733",  # Fondo activo
            activeforeground="#FFFFFF"  # Texto activo
        )
        preview_button.grid(row=0, column=3, padx=10, pady=5)  # Posiciona el botón

    def clear_search(self):
        """Limpia el filtro de búsqueda y restablece la lista completa."""
        self.search_entry.delete(0, tk.END)  # Limpiar el campo de búsqueda
        self.load_books()  # Cargar la lista completa de libros

    def load_books(self):
        """Carga todos los libros en la tabla."""

        self.clear_table()  # Limpia la tabla antes de insertar nuevos datos
        self.books = fetch_books()  # Llama a fetch_books para obtener los libros

        if not self.books:
            logging.debug("[DEBUG] No se encontraron libros en la base de datos.")

        for book in self.books:
            # book contiene: (id, titulo, autor (nombre), genero, isbn, precio, stock)
            book_id, titulo, autor, genero, isbn, precio, stock = book

            # Inserta los datos con el nombre del autor en lugar de su ID
            self.table.insert("", "end", values=(book_id, titulo, autor, genero, isbn, precio, stock))

    def search_books(self):
        """Busca libros por título."""
        query = self.search_entry.get()
        self.clear_table()
        self.books = search_books(query)
        for book in self.books:
            self.table.insert("", "end", values=book)

    def clear_table(self):
        """Limpia los datos de la tabla."""
        for row in self.table.get_children():
            self.table.delete(row)

    def load_book_for_edit(self, event):
        """Carga el libro seleccionado para editar."""
        selected_item = self.table.selection()
        if not selected_item:
            print("[DEBUG] No se seleccionó ningún libro en la tabla.")
            return  # Asegúrate de que haya un libro seleccionado

        # Obtener los datos del libro seleccionado
        selected_item_id = selected_item[0]
        book_data = self.table.item(selected_item_id, "values")

        print(f"[DEBUG] Libro seleccionado: {book_data}")

        # Cambiar a la vista de formulario y cargar los datos
        self.root.show_form()  # Cambiar la vista al formulario
        self.root.form_view.load_book_data(book_data)  # Cargar los datos en el formulario

    def delete_selected_book(self):
        """Elimina el libro seleccionado en la tabla."""
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Eliminar libro", "Por favor, selecciona un libro para eliminar.")
            return

        # Obtener los datos del libro seleccionado
        selected_item_id = selected_item[0]
        book_data = self.table.item(selected_item_id, "values")
        book_id = book_data[0]

        # Confirmación antes de eliminar
        confirm = messagebox.askyesno(
            "Eliminar libro",
            f"¿Estás seguro de que deseas eliminar el libro '{book_data[1]}'?"
        )
        if not confirm:
            return

        # Eliminar el libro de la base de datos
        try:
            delete_book(book_id)
            messagebox.showinfo("Eliminar libro", "El libro ha sido eliminado correctamente.")
            self.load_books()  # Recargar los libros en la tabla
        except Exception as e:
            messagebox.showerror("Error al eliminar", f"No se pudo eliminar el libro. Error: {e}")

    def export_to_csv(self):
        """Exporta el listado de libros a un archivo CSV."""
        if not self.books:
            messagebox.showwarning("Exportar", "No hay datos para exportar.")
            return

        # Seleccionar la ubicación y nombre del archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Guardar listado de libros"
        )

        if not file_path:
            return  # Si el usuario cancela, salir del método

        try:
            # Escribir los datos en un archivo CSV
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=";")
                # Escribir los encabezados
                writer.writerow(["ID", "Título", "Autor", "Género", "ISBN", "Precio", "Stock"])
                # Escribir los datos
                for book in self.books:
                    writer.writerow(book)

            messagebox.showinfo("Exportar", f"Listado exportado correctamente a:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el archivo. Error: {e}")

    def print_books(self):
            """Imprime el listado de libros."""
            confirm = messagebox.askyesno(
                "Confirmar impresión",
                "¿Estás seguro de que deseas imprimir el listado de libros?"
            )
            if not confirm:
                return

            if not self.books:
                messagebox.showwarning("Imprimir", "No hay datos para imprimir.")
                return

            # Crear un archivo temporal con el listado de libros
            try:
                # Seleccionar una ubicación temporal para guardar el archivo
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    title="Guardar listado para impresión"
                )

                if not file_path:
                    return  # Si el usuario cancela, salir del método

                # Escribir los datos en el archivo de texto
                with open(file_path, mode="w", encoding="utf-8") as file:
                    file.write("Listado de Libros\n")
                    file.write("=" * 50 + "\n")
                    file.write(f"{'ID':<5} {'Título':<30} {'Autor':<20} {'Género':<15} {'Precio':<10} {'Stock':<5}\n")
                    file.write("=" * 50 + "\n")
                    for book in self.books:
                        file.write(
                            f"{book[0]:<5} {book[1]:<30} {book[2]:<20} {book[3]:<15} "
                            f"{book[4]:<15} {float(book[5]):<10.2f} {int(book[6]):<5}\n"
                        )

                # Abrir el archivo con el programa predeterminado para impresión
                os.startfile(file_path, "print")

                messagebox.showinfo("Imprimir", "El listado ha sido enviado a la impresora.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo imprimir el listado. Error: {e}")

    def preview_books(self):
        """Muestra una vista previa del listado de libros antes de imprimir."""
        if not self.books:
            messagebox.showwarning("Vista Previa", "No hay datos para mostrar en la vista previa.")
            return

        # Crear una nueva ventana para la vista previa
        preview_window = tk.Toplevel(self)
        preview_window.title("Vista Previa de Impresión")
        preview_window.geometry("800x600")
        preview_window.transient(self)  # Hace que la ventana sea modal

        # Título de la vista previa
        title_label = tk.Label(preview_window, text="Vista Previa del Listado de Libros", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Caja de texto para mostrar la vista previa
        text_area = tk.Text(preview_window, wrap=tk.NONE, font=("Courier", 10))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbars
        x_scroll = ttk.Scrollbar(preview_window, orient=tk.HORIZONTAL, command=text_area.xview)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        y_scroll = ttk.Scrollbar(preview_window, orient=tk.VERTICAL, command=text_area.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.config(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

        # Generar el contenido para la vista previa
        preview_content = "Listado de Libros".center(80, "=") + "\n\n"
        preview_content += f"{'ID':<5} {'Título':<30} {'Autor':<20} {'Género':<15} {'Precio':<10} {'Stock':<5}\n"
        preview_content += "-" * 80 + "\n"

        for book in self.books:
            # Manejar valores correctamente según las columnas
            book_id = book[0]
            titulo = book[1]
            autor = book[2]
            genero = book[3]
            isbn = book[4]  # Esto no se usa en el formato
            precio = float(book[5]) if isinstance(book[5], (float, int)) or book[5].replace('.', '',
                                                                                            1).isdigit() else 0.0
            stock = int(book[6]) if isinstance(book[6], int) or book[6].isdigit() else 0

            preview_content += (
                f"{book_id:<5} {titulo:<30.29} {autor:<20.19} {genero:<15} "
                f"{precio:<10.2f} {stock:<5}\n"
            )
            preview_content += "-" * 80 + "\n"

        preview_content += f"\n{'Total de Libros:':<30} {len(self.books):<5}\n"

        # Insertar contenido en el área de texto
        text_area.insert(tk.END, preview_content)
        text_area.config(state=tk.DISABLED)  # Hacer que la vista previa sea de solo lectura

        # Botón para cerrar la vista previa
        close_button = tk.Button(preview_window, text="Cerrar", command=preview_window.destroy, bg="#A90A0A",
                                 fg="white")
        close_button.pack(pady=10)

        # Botón para proceder a imprimir
        print_button = tk.Button(preview_window, text="Imprimir", command=self.print_books, bg="#3498DB", fg="white")
        print_button.pack(pady=10)

class AuthorForm(tk.Frame):
    """Formulario para la gestión de autores."""
    def __init__(self, root=None):
        super().__init__(root, bg="#F7F7F7")
        self.root = root
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Tabla de autores
        self.create_table()

    def create_table(self):
        label = tk.Label(self, text="Lista de Autores", font=("Arial", 18, "bold"), bg="#F7F7F7")
        label.pack(pady=10)

        self.table = ttk.Treeview(self, columns=("ID", "Nombre", "Nacionalidad"))
        self.table.heading("#0", text="")
        self.table.heading("ID", text="ID")
        self.table.heading("Nombre", text="Nombre")
        self.table.heading("Nacionalidad", text="Nacionalidad")
        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_authors()

    def load_authors(self):
        self.clear_table()
        authors = fetch_authors()
        for author in authors:
            self.table.insert("", "end", values=author)

    def clear_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

class SalesView(tk.Frame):
    """Vista para gestionar y visualizar ventas."""

    def __init__(self, root=None):
        super().__init__(root, bg="#F7F7F7")
        self.root = root
        self.sales = []
        self.create_widgets()
        self.load_sales()

    def create_widgets(self):
        """Crea los widgets para la vista de ventas."""
        # Título principal
        title = tk.Label(
            self,
            text="Gestión de Ventas",
            font=("Helvetica", 18, "bold"),
            bg="#F7F7F7",
            fg="#1C5D8B"
        )
        title.pack(pady=20)

        # Contenedor de la tabla
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbars
        x_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        y_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Tabla de ventas
        self.table = ttk.Treeview(
            table_frame,
            columns=("ID", "Título", "Cantidad", "Fecha", "Monto Total"),
            show="headings",
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set
        )
        x_scroll.config(command=self.table.xview)
        y_scroll.config(command=self.table.yview)

        self.table.heading("ID", text="ID")
        self.table.heading("Título", text="Título")
        self.table.heading("Cantidad", text="Cantidad")
        self.table.heading("Fecha", text="Fecha")
        self.table.heading("Monto Total", text="Monto Total")

        self.table.column("ID", width=50, anchor="center")
        self.table.column("Título", width=200, anchor="w")
        self.table.column("Cantidad", width=100, anchor="center")
        self.table.column("Fecha", width=150, anchor="center")
        self.table.column("Monto Total", width=150, anchor="e")

        self.table.pack(fill=tk.BOTH, expand=True)

        # Botón para agregar venta
        add_button = tk.Button(
            self,
            text="Agregar Venta",
            command=self.open_add_sale_form,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 12, "bold"),
            cursor="hand2",
            activebackground="#45A049",
            activeforeground="#FFFFFF"
        )
        add_button.pack(pady=10)

        # Botón para mostrar vista previa del reporte
        preview_button = tk.Button(
            self,
            text="Vista Previa del Reporte",
            command=self.preview_sales_report,
            font=("Helvetica", 12, "bold"),
            bg="#F39C12",
            fg="#FFFFFF",
            cursor="hand2",
            activebackground="#F7B733",
            activeforeground="#FFFFFF"
        )
        preview_button.pack(pady=10)

    def load_sales(self):
        """Carga todas las ventas en la tabla."""
        self.clear_table()  # Limpia los datos existentes en la tabla
        self.sales = fetch_sales()  # Obtén las ventas con los títulos de los libros
        for sale in self.sales:
            self.table.insert("", "end", values=sale)

    def clear_table(self):
        """Limpia los datos de la tabla."""
        for row in self.table.get_children():
            self.table.delete(row)

    def show_sales_report(self):
        """Muestra un mensaje con el reporte consolidado de ventas."""
        report = fetch_sales_report()  # Implementa esta función en models.py
        if not report:
            messagebox.showinfo("Reporte de Ventas", "No hay datos disponibles.")
            return

        report_message = "Reporte Consolidado de Ventas\n\n"
        for item in report:
            titulo, total_vendido, total_ganado = item
            report_message += f"Título: {titulo}\nCantidad Vendida: {total_vendido}\nTotal Ganado: ${total_ganado:.2f}\n\n"

        messagebox.showinfo("Reporte de Ventas", report_message)

    def open_add_sale_form(self):
        """Abre un formulario para agregar una nueva venta."""
        self.add_sale_window = tk.Toplevel(self)
        self.add_sale_window.title("Agregar Venta")
        self.add_sale_window.geometry("400x300")

        # Crear el formulario
        self.create_add_sale_form(self.add_sale_window)

    def create_add_sale_form(self, parent):
        """Crea el formulario para agregar una nueva venta."""
        # Campo para seleccionar el libro
        book_label = tk.Label(parent, text="Libro:")
        book_label.grid(row=0, column=0, padx=10, pady=10)

        self.book_combobox = ttk.Combobox(parent, values=self.get_books_titles())
        self.book_combobox.grid(row=0, column=1, padx=10, pady=10)

        # Campo para ingresar la cantidad
        quantity_label = tk.Label(parent, text="Cantidad:")
        quantity_label.grid(row=1, column=0, padx=10, pady=10)

        self.quantity_entry = tk.Entry(parent)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        # Botón para guardar
        save_button = tk.Button(
            parent, text="Guardar", command=self.save_sale, bg="#4CAF50", fg="white"
        )
        save_button.grid(row=2, column=0, columnspan=2, pady=20)

    def get_books_titles(self):
        """Obtiene los títulos de los libros."""
        books = fetch_books()  # Debe estar definido en models.py
        return [book[1] for book in books]

    def save_sale(self):
        """Guarda una nueva venta en la base de datos."""
        try:
            libro = self.book_combobox.get()
            cantidad = int(self.quantity_entry.get())
            fecha = "2024-12-10"  # Usa `datetime` para obtener la fecha actual

            # Obtener el precio del libro desde la base de datos
            libro_data = next(book for book in fetch_books() if book[1] == libro)
            precio = libro_data[5]
            monto_total = cantidad * precio

            # Guardar la venta
            insert_sale((libro_data[0], cantidad, fecha, monto_total))  # Defínelo en models.py
            messagebox.showinfo("Éxito", "Venta registrada correctamente.")
            self.load_sales()  # Recargar la tabla de ventas
            self.add_sale_window.destroy()  # Cerrar el formulario
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la venta. {e}")

    def preview_sales_report(self):
        """Muestra una vista previa del reporte de ventas antes de imprimir."""
        if not self.sales:
            messagebox.showwarning("Vista Previa", "No hay datos de ventas para mostrar.")
            return

        # Crear una nueva ventana para la vista previa
        preview_window = tk.Toplevel(self)
        preview_window.title("Vista Previa de Reporte de Ventas")
        preview_window.geometry("800x600")
        preview_window.transient(self)  # Hace que la ventana sea modal

        # Título de la vista previa
        title_label = tk.Label(preview_window, text="Vista Previa del Reporte de Ventas", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Caja de texto para mostrar la vista previa
        text_area = tk.Text(preview_window, wrap=tk.NONE, font=("Courier", 10))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbars
        x_scroll = ttk.Scrollbar(preview_window, orient=tk.HORIZONTAL, command=text_area.xview)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        y_scroll = ttk.Scrollbar(preview_window, orient=tk.VERTICAL, command=text_area.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.config(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

        # Generar el contenido para la vista previa
        preview_content = "Reporte Consolidado de Ventas\n".center(80, "=") + "\n\n"
        preview_content += f"{'ID':<5} {'Título':<30} {'Cantidad':<10} {'Fecha':<15} {'Monto Total':<15}\n"
        preview_content += "-" * 80 + "\n"

        # Variables para los totales
        total_ventas = 0
        total_unidades = 0
        monto_total = 0.0

        # Procesar cada venta y generar contenido
        for sale in self.sales:
            sale_id, titulo, cantidad, fecha, monto_total_venta = sale
            preview_content += (
                f"{sale_id:<5} {titulo:<30.29} {cantidad:<10} {fecha:<15} ${monto_total_venta:<15.2f}\n"
            )
            total_ventas += 1
            total_unidades += cantidad
            monto_total += monto_total_venta

        # Agregar líneas separadoras
        preview_content += "-" * 80 + "\n"

        # Agregar los totales al final
        preview_content += f"\n{'Total de Ventas:':<30} {total_ventas:<5}\n"
        preview_content += f"{'Total de Unidades Vendidas:':<30} {total_unidades:<5}\n"
        preview_content += f"{'Monto Total Generado:':<30} ${monto_total:<10.2f}\n"

        # Insertar contenido en el área de texto
        text_area.insert(tk.END, preview_content)
        text_area.config(state=tk.DISABLED)  # Hacer que la vista previa sea de solo lectura

        # Botón para cerrar la vista previa
        close_button = tk.Button(preview_window, text="Cerrar", command=preview_window.destroy, bg="#A90A0A",
                                 fg="white")
        close_button.pack(pady=10)

        # Botón para proceder a imprimir
        print_button = tk.Button(preview_window, text="Imprimir", command=self.print_sales_report, bg="#3498DB",
                                 fg="white")
        print_button.pack(pady=10)

    def print_sales_report(self):
        """Imprime el reporte consolidado de ventas."""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Guardar reporte para impresión"
            )

            if not file_path:
                return

            with open(file_path, mode="w", encoding="utf-8") as file:
                file.write("Reporte Consolidado de Ventas\n".center(80, "=") + "\n\n")
                file.write(f"{'ID':<5} {'Título':<30} {'Cantidad':<10} {'Fecha':<15} {'Monto Total':<15}\n")
                file.write("-" * 80 + "\n")

                # Variables para los totales
                total_ventas = 0
                total_unidades = 0
                monto_total = 0.0

                # Procesar cada venta
                for sale in self.sales:
                    sale_id, titulo, cantidad, fecha, monto_total_venta = sale
                    file.write(
                        f"{sale_id:<5} {titulo:<30.29} {cantidad:<10} {fecha:<15} ${monto_total_venta:<15.2f}\n"
                    )
                    total_ventas += 1
                    total_unidades += cantidad
                    monto_total += monto_total_venta

                # Agregar totales al final
                file.write("-" * 80 + "\n")
                file.write(f"\n{'Total de Ventas:':<30} {total_ventas:<5}\n")
                file.write(f"{'Total de Unidades Vendidas:':<30} {total_unidades:<5}\n")
                file.write(f"{'Monto Total Generado:':<30} ${monto_total:<10.2f}\n")

            os.startfile(file_path, "print")
            messagebox.showinfo("Imprimir", "El reporte ha sido enviado a la impresora.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo imprimir el reporte. Error: {e}")

