"""
Script de inicialización — ejecutar UNA sola vez.
Crea la base de datos inventario_db y todas sus tablas.

Uso:
    venv/Scripts/python scripts/init_db.py
"""
import pyodbc
import os
from pathlib import Path
from dotenv import load_dotenv

# Carga el .env desde la raíz del proyecto
load_dotenv(Path(__file__).parent.parent / '.env')


def crear_base_de_datos():
    """Conecta a master y crea inventario_db si no existe."""
    servidor = os.getenv('DATABASE_URL', '').split('SERVER=')[1].split(';')[0]

    conn_master = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={servidor};'
        f'DATABASE=master;'
        f'Trusted_Connection=yes;'
    )
    # autocommit=True es necesario para CREATE DATABASE fuera de una transacción
    conn_master.autocommit = True

    cursor = conn_master.cursor()
    cursor.execute("SELECT name FROM sys.databases WHERE name = 'inventario_db'")

    if cursor.fetchone():
        print('La base de datos inventario_db ya existe, omitiendo creación.')
    else:
        cursor.execute('CREATE DATABASE inventario_db')
        print('Base de datos inventario_db creada correctamente.')

    conn_master.close()


def ejecutar_schema():
    """Lee sql/schema.sql y ejecuta cada sentencia en inventario_db."""
    ruta_schema = Path(__file__).parent.parent / 'sql' / 'schema.sql'
    sql_completo = ruta_schema.read_text(encoding='utf-8')

    # Divide el script en sentencias individuales (separa por líneas vacías o GO)
    sentencias = [s.strip() for s in sql_completo.split(';') if s.strip()]

    conn_string = os.getenv('DATABASE_URL')
    conn = pyodbc.connect(conn_string)
    conn.autocommit = True
    cursor = conn.cursor()

    for sentencia in sentencias:
        # Elimina las líneas de comentarios y verifica que quede SQL real
        lineas_sql = [l for l in sentencia.splitlines() if not l.strip().startswith('--')]
        sql_limpio = '\n'.join(lineas_sql).strip()
        if not sql_limpio:
            continue
        try:
            sentencia = sql_limpio
            cursor.execute(sentencia)
            print(f'  OK: {sentencia[:60].replace(chr(10), " ")}...')
        except pyodbc.ProgrammingError as e:
            # Si la tabla ya existe, lo reporta pero continúa
            if 'already an object' in str(e) or '2714' in str(e):
                print(f'  OMITIDO (ya existe): {sentencia[:50].replace(chr(10), " ")}...')
            else:
                raise

    conn.close()


if __name__ == '__main__':
    print('=== Inicializando base de datos ===')
    crear_base_de_datos()
    print('\n=== Creando tablas ===')
    ejecutar_schema()
    print('\n¡Listo! La base de datos está configurada.')
