import pyodbc
import os


def get_connection():
    """Abre y retorna una conexión a SQL Server."""
    connection_string = os.getenv('DATABASE_URL')
    if not connection_string:
        raise RuntimeError('DATABASE_URL no está definida en el archivo .env')
    return pyodbc.connect(connection_string)


def ejecutar_consulta(sql, params=None, fetchall=True):
    """
    Ejecuta una consulta SELECT y retorna los resultados como lista de dicts.
    Usar para operaciones de solo lectura.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params or [])

        columnas = [col[0] for col in cursor.description]
        filas = cursor.fetchall() if fetchall else [cursor.fetchone()]

        # Convierte cada fila en un diccionario {columna: valor}
        return [dict(zip(columnas, fila)) for fila in filas if fila]


def ejecutar_comando(sql, params=None):
    """
    Ejecuta un INSERT, UPDATE o DELETE.
    Retorna el número de filas afectadas.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params or [])
        filas_afectadas = cursor.rowcount
        conn.commit()
        return filas_afectadas
