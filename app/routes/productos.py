from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import ejecutar_consulta, ejecutar_comando

bp = Blueprint('productos', __name__, url_prefix='/productos')


def _cargar_categorias():
    """Carga las categorías para el select del formulario."""
    return ejecutar_consulta('SELECT id, nombre FROM categorias ORDER BY nombre')


@bp.route('/')
def lista():
    productos = ejecutar_consulta('''
        SELECT p.*, c.nombre AS categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        ORDER BY p.nombre
    ''')
    return render_template('productos/lista.html', productos=productos)


@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    categorias = _cargar_categorias()

    if request.method == 'POST':
        datos, error = _validar_form(request.form)
        if error:
            flash(error, 'danger')
            return render_template('productos/form.html', producto=None, categorias=categorias)

        ejecutar_comando('''
            INSERT INTO productos (nombre, descripcion, precio, stock, stock_minimo, categoria_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', [datos['nombre'], datos['descripcion'], datos['precio'],
              datos['stock'], datos['stock_minimo'], datos['categoria_id']])

        flash(f'Producto "{datos["nombre"]}" creado correctamente.', 'success')
        return redirect(url_for('productos.lista'))

    return render_template('productos/form.html', producto=None, categorias=categorias)


@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    resultado = ejecutar_consulta('SELECT * FROM productos WHERE id = ?', [id], fetchall=False)
    if not resultado:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('productos.lista'))

    producto = resultado[0]
    categorias = _cargar_categorias()

    if request.method == 'POST':
        datos, error = _validar_form(request.form)
        if error:
            flash(error, 'danger')
            return render_template('productos/form.html', producto=producto, categorias=categorias)

        ejecutar_comando('''
            UPDATE productos
            SET nombre = ?, descripcion = ?, precio = ?,
                stock = ?, stock_minimo = ?, categoria_id = ?,
                actualizado_en = GETDATE()
            WHERE id = ?
        ''', [datos['nombre'], datos['descripcion'], datos['precio'],
              datos['stock'], datos['stock_minimo'], datos['categoria_id'], id])

        flash(f'Producto "{datos["nombre"]}" actualizado correctamente.', 'success')
        return redirect(url_for('productos.lista'))

    return render_template('productos/form.html', producto=producto, categorias=categorias)


@bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    resultado = ejecutar_consulta('SELECT nombre FROM productos WHERE id = ?', [id], fetchall=False)
    if not resultado:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('productos.lista'))

    nombre = resultado[0]['nombre']
    ejecutar_comando('DELETE FROM productos WHERE id = ?', [id])
    flash(f'Producto "{nombre}" eliminado.', 'warning')
    return redirect(url_for('productos.lista'))


def _validar_form(form):
    """
    Valida y convierte los datos del formulario.
    Retorna (datos_dict, None) si todo está bien, o (None, mensaje_error).
    """
    nombre = form.get('nombre', '').strip()
    if not nombre:
        return None, 'El nombre es obligatorio.'

    try:
        precio = float(form.get('precio', 0))
        if precio < 0:
            raise ValueError
    except ValueError:
        return None, 'El precio debe ser un número mayor o igual a 0.'

    try:
        stock = int(form.get('stock', 0))
        if stock < 0:
            raise ValueError
    except ValueError:
        return None, 'El stock debe ser un número entero mayor o igual a 0.'

    try:
        stock_minimo = int(form.get('stock_minimo', 5))
        if stock_minimo < 0:
            raise ValueError
    except ValueError:
        return None, 'El stock mínimo debe ser un número entero mayor o igual a 0.'

    categoria_id = form.get('categoria_id') or None
    if categoria_id:
        categoria_id = int(categoria_id)

    return {
        'nombre':       nombre,
        'descripcion':  form.get('descripcion', '').strip() or None,
        'precio':       precio,
        'stock':        stock,
        'stock_minimo': stock_minimo,
        'categoria_id': categoria_id,
    }, None
