from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import ejecutar_consulta, ejecutar_transaccion

bp = Blueprint('movimientos', __name__, url_prefix='/movimientos')


@bp.route('/')
def lista():
    movimientos = ejecutar_consulta('''
        SELECT m.*, p.nombre AS producto_nombre
        FROM movimientos m
        JOIN productos p ON m.producto_id = p.id
        ORDER BY m.fecha DESC
    ''')
    return render_template('movimientos/lista.html', movimientos=movimientos)


@bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    productos = ejecutar_consulta('SELECT id, nombre, stock FROM productos ORDER BY nombre')

    if request.method == 'POST':
        producto_id = request.form.get('producto_id', '').strip()
        tipo = request.form.get('tipo', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        # Validaciones básicas
        if not producto_id:
            flash('Debes seleccionar un producto.', 'danger')
            return render_template('movimientos/form.html', productos=productos)

        if tipo not in ('entrada', 'salida'):
            flash('El tipo debe ser entrada o salida.', 'danger')
            return render_template('movimientos/form.html', productos=productos)

        try:
            cantidad = int(request.form.get('cantidad', 0))
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            flash('La cantidad debe ser un número entero mayor a 0.', 'danger')
            return render_template('movimientos/form.html', productos=productos)

        # Para salidas: verificar que haya suficiente stock
        if tipo == 'salida':
            resultado = ejecutar_consulta(
                'SELECT stock, nombre FROM productos WHERE id = ?',
                [producto_id], fetchall=False
            )
            if not resultado:
                flash('Producto no encontrado.', 'danger')
                return render_template('movimientos/form.html', productos=productos)

            stock_actual = resultado[0]['stock']
            nombre_producto = resultado[0]['nombre']

            if stock_actual < cantidad:
                flash(
                    f'Stock insuficiente para "{nombre_producto}". '
                    f'Stock actual: {stock_actual}, solicitado: {cantidad}.',
                    'danger'
                )
                return render_template('movimientos/form.html', productos=productos)

        # Transacción atómica: registrar movimiento y actualizar stock
        ajuste = cantidad if tipo == 'entrada' else -cantidad

        ejecutar_transaccion([
            (
                'INSERT INTO movimientos (producto_id, tipo, cantidad, descripcion) VALUES (?, ?, ?, ?)',
                [producto_id, tipo, cantidad, descripcion or None]
            ),
            (
                'UPDATE productos SET stock = stock + ?, actualizado_en = GETDATE() WHERE id = ?',
                [ajuste, producto_id]
            ),
        ])

        accion = 'registrada' if tipo == 'entrada' else 'registrada'
        flash(f'{tipo.capitalize()} de {cantidad} unidad(es) {accion} correctamente.', 'success')
        return redirect(url_for('movimientos.lista'))

    return render_template('movimientos/form.html', productos=productos)
