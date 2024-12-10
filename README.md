import tkinter as tk
from tkinter import ttk


class BookForm(tk.Frame):
    """Formulario para la gestión de libros."""

    def __init__(self, root=None):
        super().__init__(root, width=800, height=600, bg='#F7F7F7')
        self.root = root
        self.pack()
        self.entries = {}
        self.create_widgets()
        self.disable_fields()

    def create_widgets(self):
        self.create_labels()
        self.create_inputs()
        self.create_buttons()

    def create_labels(self):
        """Crea las etiquetas del formulario."""
        labels = ['Título:', 'Autor:', 'Género:', 'ISBN:', 'Precio:', 'Stock:']
        for idx, text in enumerate(labels):
            label = tk.Label(self, text=text, font=('Arial', 12, 'bold'), bg='#F7F7F7')
            label.grid(row=idx, column=0, padx=10, pady=10, sticky='e')

    def create_inputs(self):
        """Crea las entradas del formulario."""
        self.entries['Título'] = tk.Entry(self, width=50)
        self.entries['Autor'] = tk.Entry(self, width=50)
        self.entries['Género'] = ttk.Combobox(
            self, values=['Ficción', 'No Ficción', 'Educativo', 'Ciencia'], state='readonly', width=48
        )
        self.entries['ISBN'] = tk.Entry(self, width=50)
        self.entries['Precio'] = tk.Entry(self, width=50)
        self.entries['Stock'] = tk.Entry(self, width=50)

        for idx, entry in enumerate(self.entries.values()):
            entry.grid(row=idx, column=1, padx=10, pady=10, columnspan=2)

    def create_buttons(self):
        """Crea los botones principales."""
        self.btn_new = tk.Button(
            self, text='Nuevo', command=self.enable_fields,
            width=15, font=('Arial', 12, 'bold'), bg='#198754', fg='white', cursor='hand2'
        )
        self.btn_new.grid(row=6, column=0, padx=10, pady=20)

        self.btn_save = tk.Button(
            self, text='Guardar', command=self.save_record,
            width=15, font=('Arial', 12, 'bold'), bg='#0D6EFD', fg='white', cursor='hand2'
        )
        self.btn_save.grid(row=6, column=1, padx=10, pady=20)

        self.btn_cancel = tk.Button(
            self, text='Cancelar', command=self.disable_fields,
            width=15, font=('Arial', 12, 'bold'), bg='#DC3545', fg='white', cursor='hand2'
        )
        self.btn_cancel.grid(row=6, column=2, padx=10, pady=20)

    def enable_fields(self):
        """Habilita los campos de entrada."""
        for entry in self.entries.values():
            entry.config(state='normal')
        self.btn_save.config(state='normal')
        self.btn_cancel.config(state='normal')
        self.btn_new.config(state='disabled')

    def disable_fields(self):
        """Deshabilita los campos de entrada."""
        for entry in self.entries.values():
            entry.config(state='disabled')
        self.btn_save.config(state='disabled')
        self.btn_cancel.config(state='disabled')
        self.btn_new.config(state='normal')

    def save_record(self):
        """Guarda el registro en la base de datos (placeholder)."""
        data = {key: entry.get() for key, entry in self.entries.items()}
        print("Datos guardados:", data)
        self.disable_fields()
