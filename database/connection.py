import sqlite3

def connect_db():
    """Establece la conexión con la base de datos."""
    conn = sqlite3.connect("libreria.db")
    conn.execute("PRAGMA foreign_keys = ON;")  # Activar claves foráneas
    return conn


def create_tables():
    """Crea las tablas necesarias en la base de datos."""
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Crear tabla de autores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS autores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                nacionalidad TEXT
               
            )
        ''')

        # Crear tabla de libros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor_id INTEGER NOT NULL,
                genero TEXT NOT NULL,
                isbn TEXT NOT NULL,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL,
                FOREIGN KEY (autor_id) REFERENCES autores (id)
            )
        ''')

        # Crear tabla de ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                libro_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                monto_total REAL NOT NULL,
                FOREIGN KEY (libro_id) REFERENCES libros (id)
            )
        ''')

        conn.commit()
    except Exception as e:
        print(f"[ERROR] Error al crear tablas: {e}")
    finally:
        conn.close()
