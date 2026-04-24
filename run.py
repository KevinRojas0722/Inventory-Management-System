from app import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True recarga el servidor automáticamente al guardar cambios
    app.run(debug=True)
