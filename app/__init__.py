from flask import Flask
from dotenv import load_dotenv
import os

# Carga las variables del archivo .env antes de crear la app
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Clave secreta para las sesiones de Flask
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-insegura')

    # Cadena de conexión a la base de datos
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

    from .routes.categorias import bp as categorias_bp
    app.register_blueprint(categorias_bp)

    from .routes.productos import bp as productos_bp
    app.register_blueprint(productos_bp)

    from .routes.movimientos import bp as movimientos_bp
    app.register_blueprint(movimientos_bp)

    return app
