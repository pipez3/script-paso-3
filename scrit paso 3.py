import hashlib
from flask import Flask, request
import sqlite3

app = Flask(__name__)
DATABASE = 'users.db'

# Configuración de la base de datos
def get_db():
    db = sqlite3.connect(DATABASE)
    db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password_hash TEXT)")
    return db

# Función para almacenar usuarios y contraseñas en hash
def store_user(username, password):
    db = get_db()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
    db.commit()
    db.close()

# Función para validar usuarios y contraseñas
def validate_user(username, password):
    db = get_db()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    result = db.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
    user = result.fetchone()
    db.close()
    return user is not None

# Ruta para almacenar usuarios y contraseñas en hash
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    store_user(username, password)
    return 'Usuario registrado exitosamente.'

# Ruta para validar usuarios y contraseñas
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if validate_user(username, password):
        return 'Inicio de sesión exitoso.'
    else:
        return 'Nombre de usuario o contraseña incorrectos.'

if __name__ == '__main__':
    app.run(port=4850)
