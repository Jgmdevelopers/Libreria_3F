import unicodedata
import logging
from database.connection import connect_db

# Funciones para autores
def fetch_authors():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM autores')
    authors = cursor.fetchall()
    conn.close()
    return authors

def insert_author(nombre, nacionalidad=None):
    """Inserta un autor en la base de datos."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO autores (nombre, nacionalidad) VALUES (?, ?)", (nombre, nacionalidad)
        )
        conn.commit()
        return cursor.lastrowid  # Retornar el ID del autor recién insertado
    except Exception as e:
        print(f"[ERROR] Error al manejar autor: {e}")
        return None
    finally:
        conn.close()

def get_author_by_name(nombre):

    """Obtiene un autor por su nombre."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM autores WHERE nombre = ?", (nombre,))
    author = cursor.fetchone()

    conn.close()
    return author

# Funciones para libros
def insert_book(data):
    """Inserta un libro en la base de datos, gestionando al autor si no existe."""
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Validar datos de entrada
        titulo_original = data[0].strip()
        autor_nombre = data[1]


        if not titulo_original:
            raise ValueError("El título no puede estar vacío.")
        if not autor_nombre or not isinstance(autor_nombre, str):
            raise ValueError(f"Nombre del autor no válido: {autor_nombre}")

        # Verificar si el autor existe
        author = get_author_by_name(autor_nombre)

        if not author:
            autor_id = insert_author(autor_nombre, None)
        else:
            autor_id = author[0]  # ID del autor existente

        # Crear datos para el libro
        book_data = (titulo_original, autor_id, *data[2:])  # (titulo, autor_id, genero, isbn, precio, stock)

        # Insertar el libro
        cursor.execute('''
            INSERT INTO libros (titulo, autor_id, genero, isbn, precio, stock)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', book_data)
        conn.commit()
    except Exception as e:
        print(f"[ERROR] Error al insertar libro: {e}")
    finally:
        conn.close()


def fetch_books():
    """Obtiene todos los libros de la base de datos."""
    conn = connect_db()
    cursor = conn.cursor()

    try:
        sql_query = '''
            SELECT 
                libros.id, 
                libros.titulo, 
                autores.nombre AS autor,
                libros.genero, 
                libros.isbn, 
                libros.precio, 
                libros.stock
            FROM libros
            JOIN autores ON libros.autor_id = autores.id
        '''
        cursor.execute(sql_query)
        books = cursor.fetchall()

        # Log para verificar los resultados obtenidos

        return books
    except Exception as e:
        # Log para registrar cualquier error en la ejecución
        return []
    finally:
        conn.close()


def update_book(book_id, data):
    """Actualiza los datos de un libro existente."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE libros
        SET titulo = ?, autor_id = ?, genero = ?, isbn = ?, precio = ?, stock = ?
        WHERE id = ?
    ''', (*data,))
    conn.commit()
    conn.close()
    print(f"[INFO] Libro con ID {book_id} actualizado correctamente.")

def delete_book(book_id):
    """Elimina un libro por su ID."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM libros WHERE id = ?', (book_id,))
        conn.commit()
        print(f"[INFO] Libro eliminado (ID: {book_id})")
    except Exception as e:
        print(f"[ERROR] Error al eliminar libro: {e}")
    finally:
        conn.close()

def remove_accents(input_str):
    """Elimina los acentos de una cadena."""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    result = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return result

def search_books(query):
    """Busca libros por título (insensible a mayúsculas y acentos)."""
    conn = connect_db()
    cursor = conn.cursor()

    # Imprimir todos los títulos para depuración
    cursor.execute('SELECT titulo FROM libros')
    all_titles = cursor.fetchall()

    # Normalizar la consulta
    query_normalized = remove_accents(query.lower())

    # Realizar la búsqueda
    sql_query = '''
        SELECT libros.id, libros.titulo, autores.nombre AS autor, libros.genero, libros.isbn, libros.precio, libros.stock
        FROM libros
        JOIN autores ON libros.autor_id = autores.id
        WHERE LOWER(libros.titulo) LIKE ?
    '''
    param = f"%{query_normalized}%"

    cursor.execute(sql_query, (param,))
    books = cursor.fetchall()

    conn.close()
    return books

# Funciones para ventas
def insert_sale(data):
    """Registra una venta y actualiza el stock del libro."""
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Desglosar los datos de la venta
        libro_id, cantidad, fecha, monto_total = data

        # Verificar si hay suficiente stock
        cursor.execute('SELECT stock FROM libros WHERE id = ?', (libro_id,))
        stock_actual = cursor.fetchone()
        if not stock_actual or stock_actual[0] < cantidad:
            raise ValueError("Stock insuficiente para realizar la venta.")

        # Registrar la venta
        cursor.execute('''
            INSERT INTO ventas (libro_id, cantidad, fecha, monto_total)
            VALUES (?, ?, ?, ?)
        ''', data)

        # Actualizar el stock
        nuevo_stock = stock_actual[0] - cantidad
        cursor.execute('UPDATE libros SET stock = ? WHERE id = ?', (nuevo_stock, libro_id))

        conn.commit()
        print(f"[INFO] Venta registrada: {data}")
    except ValueError as ve:
        print(f"[ERROR] {ve}")
    except Exception as e:
        print(f"[ERROR] Error al registrar venta: {e}")
    finally:
        conn.close()

def fetch_sales():
    """Obtiene todas las ventas con los títulos de los libros."""
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
        SELECT ventas.id, libros.titulo, ventas.cantidad, ventas.fecha, ventas.monto_total
        FROM ventas
        JOIN libros ON ventas.libro_id = libros.id
    '''
    cursor.execute(query)
    sales = cursor.fetchall()
    conn.close()
    return sales

def fetch_sales_by_book(libro_id):
    """Obtiene todas las ventas de un libro específico."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT ventas.id, libros.titulo, ventas.cantidad, ventas.fecha, ventas.monto_total
            FROM ventas
            JOIN libros ON ventas.libro_id = libros.id
            WHERE ventas.libro_id = ?
        ''', (libro_id,))
        sales = cursor.fetchall()
        return sales
    except Exception as e:
        print(f"[ERROR] Error al obtener ventas del libro: {e}")
        return []
    finally:
        conn.close()

def fetch_sales_report():
    """Genera un reporte consolidado de ventas agrupado por libro."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT libros.titulo, SUM(ventas.cantidad) AS total_vendido, SUM(ventas.monto_total) AS total_ganado
            FROM ventas
            JOIN libros ON ventas.libro_id = libros.id
            GROUP BY libros.titulo
            ORDER BY total_vendido DESC
        ''')
        report = cursor.fetchall()
        return report
    except Exception as e:
        print(f"[ERROR] Error al generar el reporte de ventas: {e}")
        return []
    finally:
        conn.close()
