# 📦 Inventory Management System

Web application to register and control the inventory of a small business. Built with Python/Flask and SQL Server.

## 🤔 What does it do?

- **Products:** create, edit and delete products with price, stock and assigned category
- **Categories:** organize products by type
- **Movements:** register inbound and outbound stock — these validate that there's enough quantity before processing
- **Dashboard:** summary with total products, inventory value, low-stock alerts and the latest registered movements

## 🛠️ Stack

- 🐍 Python + Flask
- 💾 SQL Server Express with Windows Authentication
- 🎨 Bootstrap 5 + custom CSS
- 🔌 pyodbc for the database connection
- 🔑 python-dotenv for handling environment variables

## 🚀 How to run it locally

> ⚠️ **Prerequisites:** having SQL Server Express installed with the `localhost\SQLEXPRESS` instance.

### 1. Clone the repository

```bash
git clone https://github.com/KevinRojas0722/inventario-app.git
cd inventario-app
```

### 2. Create and activate the virtual environment

```bash
python -m venv venv
venv/Scripts/activate     # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` if your SQL Server instance has a different name than `localhost\SQLEXPRESS`.

### 5. Create the database

```bash
python scripts/init_db.py
```

### 6. Start the server

```bash
python run.py
```

🌐 Open `http://127.0.0.1:5000` in your browser.

## 📁 Project structure

```
inventario-app/
├── app/
│   ├── routes/                # Blueprints (categories, products, movements, dashboard)
│   ├── templates/             # HTML with Jinja2
│   ├── static/                # CSS
│   ├── database.py            # Database connection layer
│   └── __init__.py            # Application factory
├── scripts/
│   └── init_db.py             # Database initialization
├── sql/
│   └── schema.sql             # Table DDL
├── .env.example
├── requirements.txt
└── run.py
```

## 💡 Technical decisions

- **Application Factory:** the Flask app is created inside a function (`create_app()`) to make configuration easier and avoid circular imports.
- **Blueprints:** each module (products, categories, movements) has its own Blueprint. This keeps the code organized and easy to scale.
- **Transactions:** when registering a movement, stock is updated atomically — if it fails, the previous quantity is restored.
- **Immutable movements:** movements cannot be edited or deleted. If there's an error, a correction movement is registered. This keeps the history reliable.

## 👤 Author

**Kevin Rojas Hernández**

🔗 [GitHub](https://github.com/KevinRojas0722) · 💼 [LinkedIn](https://www.linkedin.com/in/kevin-rojas-hernandez-dev) · 📧 kevinrh2000@gmail.com
