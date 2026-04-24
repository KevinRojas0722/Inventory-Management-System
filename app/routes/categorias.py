from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import ejecutar_consulta, ejecutar_comando

bp = Blueprint('categorias', __name__, url_prefix='/categorias')


@bp.route('/')
def lista():
    categorias = ejecutar_consulta('SELECT * FROM categorias ORDER BY nombre')
    return render_template('categorias/lista.html', categorias=categorias)


@bp.route('/nueva', methods=['GET', 'POST'])
def nueva():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        if not nombre:
            flash('El nombre es obligatorio.', 'danger')
            return render_template('categorias/form.html', categoria=None)

        ejecutar_comando(
            'INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)',
            [nombre, descripcion or None]
        )
        flash(f'Categoría "{nombre}" creada correctamente.', 'success')
        return redirect(url_for('categorias.lista'))

    return render_template('categorias/form.html', categoria=None)


@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    resultado = ejecutar_consulta('SELECT * FROM categorias WHERE id = ?', [id], fetchall=False)
    if not resultado:
        flash('Categoría no encontrada.', 'danger')
        return redirect(url_for('categorias.lista'))

    categoria = resultado[0]

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        if not nombre:
            flash('El nombre es obligatorio.', 'danger')
            return render_template('categorias/form.html', categoria=categoria)

        ejecutar_comando(
            'UPDATE categorias SET nombre = ?, descripcion = ? WHERE id = ?',
            [nombre, descripcion or None, id]
        )
        flash(f'Categoría "{nombre}" actualizada correctamente.', 'success')
        return redirect(url_for('categorias.lista'))

    return render_template('categorias/form.html', categoria=categoria)


@bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    resultado = ejecutar_consulta('SELECT nombre FROM categorias WHERE id = ?', [id], fetchall=False)
    if not resultado:
        flash('Categoría no encontrada.', 'danger')
        return redirect(url_for('categorias.lista'))

    nombre = resultado[0]['nombre']
    ejecutar_comando('DELETE FROM categorias WHERE id = ?', [id])
    flash(f'Categoría "{nombre}" eliminada.', 'warning')
    return redirect(url_for('categorias.lista'))
