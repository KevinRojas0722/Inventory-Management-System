# Sistema de Gestión de Inventario

Aplicación web para registrar y controlar el inventario de un negocio. Hecha con Python/Flask y SQL Server como proyecto de portafolio.

## ¿Qué hace?

- **Productos**: crear, editar y eliminar productos con precio, stock y categoría asignada
- **Categorías**: organizar los productos por tipo
- **Movimientos**: registrar entradas y salidas de stock — las salidas validan que haya suficiente cantidad antes de procesarse
- **Dashboard**: resumen con total de productos, valor del inventario, alertas de bajo stock y los últimos movimientos registrados

## Stack

- Python + Flask
- SQL Server Express con Windows Authentication
- Bootstrap 5 + CSS personalizado
- pyodbc para la conexión con la base de datos
- python-dotenv para manejar variables de entorno

## Cómo correrlo localmente

**Requisitos previos:** tener SQL Server Express instalado con la instancia `SQLEXPRESS`.

1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/inventario-app.git
cd inventario-app
```

2. Crear y activar el entorno virtual

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

3. Instalar dependencias

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` si tu instancia de SQL Server tiene un nombre diferente a `localhost\SQLEXPRESS`.

5. Crear la base de datos

```bash
python scripts/init_db.py
```

6. Arrancar el servidor

```bash
python run.py
```

Abrir `http://127.0.0.1:5000` en el navegador.

## Estructura del proyecto

```
inventario-app/
├── app/
│   ├── routes/          # Blueprints (categorías, productos, movimientos, dashboard)
│   ├── templates/       # HTML con Jinja2
│   ├── static/          # CSS
│   ├── database.py      # Capa de acceso a datos
│   └── __init__.py      # Application Factory
├── scripts/
│   └── init_db.py       # Inicialización de la base de datos
├── sql/
│   └── schema.sql       # DDL de las tablas
├── .env.example
├── requirements.txt
└── run.py
```

## Decisiones técnicas

- **Application Factory**: la app de Flask se crea dentro de una función `create_app()` para facilitar la configuración y evitar importaciones circulares.
- **Blueprints**: cada módulo (productos, categorías, movimientos) tiene su propio Blueprint. Así el código no termina todo en un solo archivo.
- **Transacciones**: registrar un movimiento actualiza el stock del producto de forma atómica — si algo falla, se hace rollback y ninguno de los dos cambios queda a medias.
- **Movimientos inmutables**: los movimientos no se pueden editar ni eliminar. Si hubo un error, se registra un movimiento correctivo. Esto mantiene un historial confiable.
