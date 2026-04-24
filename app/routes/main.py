from flask import Blueprint, render_template
from app.database import ejecutar_consulta

bp = Blueprint('main', __name__)


@bp.route('/')
def dashboard():
    # Una sola query trae los 4 números del encabezado
    resumen = ejecutar_consulta('''
        SELECT
            COUNT(*)                        AS total_productos,
            COALESCE(SUM(precio * stock), 0) AS valor_inventario,
            SUM(CASE WHEN stock <= stock_minimo AND stock > 0 THEN 1 ELSE 0 END) AS bajo_stock,
            SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END) AS sin_stock
        FROM productos
    ''', fetchall=False)[0]

    # Productos que necesitan reabastecimiento
    productos_alerta = ejecutar_consulta('''
        SELECT p.nombre, p.stock, p.stock_minimo, c.nombre AS categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.stock <= p.stock_minimo
        ORDER BY p.stock ASC
    ''')

    # Historial reciente
    ultimos_movimientos = ejecutar_consulta('''
        SELECT TOP 8 m.tipo, m.cantidad, m.fecha, m.descripcion, p.nombre AS producto_nombre
        FROM movimientos m
        JOIN productos p ON m.producto_id = p.id
        ORDER BY m.fecha DESC
    ''')

    return render_template('dashboard.html',
                           resumen=resumen,
                           productos_alerta=productos_alerta,
                           ultimos_movimientos=ultimos_movimientos)
