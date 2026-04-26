# app.py - Sistema SaaS para Contadores (Flask + SQLite)
# Ejecutar: python app.py

import io
import os
import sqlite3
import zipfile
from contextlib import contextmanager
from datetime import datetime
from functools import wraps

from flask import Flask, redirect, render_template_string, request, send_file, session, url_for
from werkzeug.utils import secure_filename

# ==================== CONFIGURACIÓN ====================
app = Flask(__name__)
app.secret_key = "clave_secreta_super_segura_2024"
DATABASE = "saas_contadores.db"
UPLOAD_FOLDER = "facturas_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==================== BASE DE DATOS ====================
def init_db():
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS configuracion (
            id INTEGER PRIMARY KEY,
            contacto TEXT DEFAULT '',
            privacidad TEXT DEFAULT '',
            info_general TEXT DEFAULT '',
            precio_mensual REAL DEFAULT 0,
            precio_semestral REAL DEFAULT 0,
            precio_anual REAL DEFAULT 0
        )"""
        )

        cursor.execute("INSERT OR IGNORE INTO configuracion (id) VALUES (1)")

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL CHECK(rol IN ('super_admin', 'contador', 'cliente')),
            contador_id INTEGER,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (contador_id) REFERENCES usuarios(id)
        )"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            imagen_path TEXT NOT NULL,
            valor REAL NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES usuarios(id)
        )"""
        )

        cursor.execute("SELECT id FROM usuarios WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                ("admin", "admin123", "super_admin"),
            )


@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ==================== FUNCIONES AUXILIARES ====================
def login_required(roles=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))
            if roles and session.get("rol") not in roles:
                return "<h1>Acceso denegado</h1>", 403
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def get_config():
    with get_db() as conn:
        return conn.execute("SELECT * FROM configuracion WHERE id = 1").fetchone()


# ==================== PLANTILLAS HTML ====================
HTML_HEADER = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SaaS Contadores</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; }
        .navbar { background: #1a237e; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .navbar h2 { font-size: 24px; }
        .nav-links { display: flex; gap: 20px; align-items: center; }
        .nav-links a { color: white; text-decoration: none; padding: 8px 15px; border-radius: 5px; transition: background 0.3s; }
        .nav-links a:hover { background: #283593; }
        .btn-logout { background: #c62828; padding: 8px 20px; border-radius: 5px; color: white; text-decoration: none; }
        .btn-logout:hover { background: #b71c1c; }
        .container { max-width: 1200px; margin: 30px auto; padding: 20px; }
        .card { background: white; border-radius: 10px; padding: 25px; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .card h3 { color: #1a237e; margin-bottom: 20px; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; color: #333; font-weight: 500; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
        .btn { padding: 10px 25px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; font-weight: bold; transition: transform 0.2s; text-decoration: none; display: inline-block; }
        .btn:hover { transform: translateY(-2px); }
        .btn-primary { background: #1a237e; color: white; }
        .btn-success { background: #2e7d32; color: white; }
        .btn-warning { background: #f57c00; color: white; }
        .btn-info { background: #0277bd; color: white; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #1a237e; color: white; }
        tr:hover { background: #f5f5f5; }
        .alert { padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .alert-error { background: #ffebee; color: #c62828; border: 1px solid #ef9a9a; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
        .stats { display: flex; gap: 20px; margin-bottom: 20px; }
        .stat-card { flex: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }
        .stat-card h2 { font-size: 36px; margin-bottom: 10px; }
        @media (max-width: 768px) { .grid-2, .grid-3 { grid-template-columns: 1fr; } .stats { flex-direction: column; } }
    </style>
</head>
<body>
"""

HTML_FOOTER = """
</body>
</html>
"""

LOGIN_TEMPLATE = HTML_HEADER + """
<div style="display: flex; justify-content: center; align-items: center; min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <div class="card" style="width: 400px;">
        <h2 style="text-align: center; color: #1a237e; margin-bottom: 30px;">🔐 SaaS Contadores</h2>
        {% if error %}
        <div class="alert alert-error">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <div class="form-group">
                <label>Usuario:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Contraseña:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">Iniciar Sesión</button>
        </form>
        <p style="text-align: center; margin-top: 20px; color: #666;">
            Admin por defecto: admin / admin123
        </p>
    </div>
</div>
""" + HTML_FOOTER

SUPER_ADMIN_TEMPLATE = HTML_HEADER + """
<div class="navbar">
    <h2>👑 Panel Super Admin</h2>
    <div class="nav-links">
        <span style="color: #ffd54f;">{{ session.username }} (Super Admin)</span>
        <a href="{{ url_for('logout') }}" class="btn-logout">Cerrar Sesión</a>
    </div>
</div>
<div class="container">
    <div class="stats">
        <div class="stat-card">
            <h2>{{ contadores|length }}</h2>
            <p>Contadores</p>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h2>{{ clientes|length }}</h2>
            <p>Clientes</p>
        </div>
    </div>

    <div class="grid-2">
        <div class="card">
            <h3>➕ Crear Contador</h3>
            <form method="POST" action="{{ url_for('crear_contador') }}">
                <div class="form-group">
                    <label>Usuario:</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>Contraseña:</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit" class="btn btn-success">Crear Contador</button>
            </form>
        </div>

        <div class="card">
            <h3>💰 Configurar Precios de Membresía</h3>
            <form method="POST" action="{{ url_for('actualizar_configuracion') }}">
                <div class="form-group">
                    <label>Precio Mensual ($):</label>
                    <input type="number" step="0.01" name="precio_mensual" value="{{ config.precio_mensual }}" required>
                </div>
                <div class="form-group">
                    <label>Precio Semestral ($):</label>
                    <input type="number" step="0.01" name="precio_semestral" value="{{ config.precio_semestral }}" required>
                </div>
                <div class="form-group">
                    <label>Precio Anual ($):</label>
                    <input type="number" step="0.01" name="precio_anual" value="{{ config.precio_anual }}" required>
                </div>
                <button type="submit" class="btn btn-primary">Guardar Precios</button>
            </form>
        </div>

        <div class="card">
            <h3>📋 Contadores Registrados</h3>
            <table>
                <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>Fecha Registro</th>
                    </tr>
                </thead>
                <tbody>
                    {% for contador in contadores %}
                    <tr>
                        <td>{{ contador.username }}</td>
                        <td>{{ contador.fecha_registro }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div class="card">
            <h3>👥 Clientes Registrados</h3>
            <table>
                <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>Contador</th>
                        <th>Fecha Registro</th>
                    </tr>
                </thead>
                <tbody>
                    {% for cliente in clientes %}
                    <tr>
                        <td>{{ cliente.username }}</td>
                        <td>{{ cliente.contador or 'Sin asignar' }}</td>
                        <td>{{ cliente.fecha_registro }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <div class="card">
        <h3>⚙️ Configuración General</h3>
        <form method="POST" action="{{ url_for('actualizar_configuracion') }}">
            <div class="grid-3">
                <div class="form-group">
                    <label>Información de Contacto:</label>
                    <textarea name="contacto" rows="4">{{ config.contacto }}</textarea>
                </div>
                <div class="form-group">
                    <label>Políticas de Privacidad:</label>
                    <textarea name="privacidad" rows="4">{{ config.privacidad }}</textarea>
                </div>
                <div class="form-group">
                    <label>Info General Plataforma:</label>
                    <textarea name="info_general" rows="4">{{ config.info_general }}</textarea>
                </div>
            </div>
            <button type="submit" class="btn btn-info">Actualizar Configuración</button>
        </form>
    </div>
</div>
""" + HTML_FOOTER

CONTADOR_TEMPLATE = HTML_HEADER + """
<div class="navbar">
    <h2>📊 Panel Contador</h2>
    <div class="nav-links">
        <span>{{ session.username }} (Contador)</span>
        <a href="{{ url_for('logout') }}" class="btn-logout">Cerrar Sesión</a>
    </div>
</div>
<div class="container">
    <div class="grid-2">
        <div class="card">
            <h3>➕ Crear Cliente</h3>
            <form method="POST" action="{{ url_for('crear_cliente') }}">
                <div class="form-group">
                    <label>Usuario del Cliente:</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>Contraseña:</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit" class="btn btn-success">Crear Cliente</button>
            </form>
        </div>

        <div class="card">
            <h3>🔍 Filtrar Facturas</h3>
            <form method="GET" action="{{ url_for('panel_contador') }}">
                <div class="form-group">
                    <label>Fecha Inicio:</label>
                    <input type="date" name="fecha_inicio" value="{{ fecha_inicio }}">
                </div>
                <div class="form-group">
                    <label>Fecha Fin:</label>
                    <input type="date" name="fecha_fin" value="{{ fecha_fin }}">
                </div>
                <button type="submit" class="btn btn-primary">Filtrar</button>
                <a href="{{ url_for('panel_contador') }}" class="btn btn-warning">Limpiar</a>
            </form>
        </div>
    </div>

    <div class="card">
        <h3>📄 Facturas de Clientes
            <span style="float: right;">
                <a href="{{ url_for('descargar_facturas_zip', fecha_inicio=fecha_inicio, fecha_fin=fecha_fin) }}" class="btn btn-info">📥 Descargar ZIP</a>
            </span>
        </h3>
        <div class="stats">
            <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <h2>{{ facturas|length }}</h2>
                <p>Total Facturas</p>
            </div>
            <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <h2>${{ "%.2f"|format(suma_total) }}</h2>
                <p>Suma Total</p>
            </div>
        </div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Cliente</th>
                    <th>Valor</th>
                    <th>Fecha</th>
                    <th>Imagen</th>
                </tr>
            </thead>
            <tbody>
                {% for factura in facturas %}
                <tr>
                    <td>{{ factura.id }}</td>
                    <td>{{ factura.cliente_nombre }}</td>
                    <td>${{ "%.2f"|format(factura.valor) }}</td>
                    <td>{{ factura.fecha }}</td>
                    <td>
                        <a href="/{{ factura.imagen_path }}" target="_blank" class="btn btn-info" style="padding: 5px 10px; font-size: 12px;">Ver</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
""" + HTML_FOOTER

CLIENTE_TEMPLATE = HTML_HEADER + """
<div class="navbar">
    <h2>📋 Panel Cliente</h2>
    <div class="nav-links">
        <span>{{ session.username }} (Cliente)</span>
        <a href="{{ url_for('logout') }}" class="btn-logout">Cerrar Sesión</a>
    </div>
</div>
<div class="container">
    <div class="card">
        <h3>📤 Subir Nueva Factura</h3>
        <form method="POST" action="{{ url_for('subir_factura') }}" enctype="multipart/form-data">
            <div class="form-group">
                <label>Imagen de Factura (JPG/PNG):</label>
                <input type="file" name="imagen" accept=".jpg,.jpeg,.png" required>
            </div>
            <div class="form-group">
                <label>Valor ($):</label>
                <input type="number" step="0.01" name="valor" required>
            </div>
            <button type="submit" class="btn btn-primary">Subir Factura</button>
        </form>
    </div>

    <div class="card">
        <h3>📊 Mi Historial de Facturas</h3>
        <div class="stats">
            <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <h2>{{ facturas|length }}</h2>
                <p>Total Facturas</p>
            </div>
            <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <h2>${{ "%.2f"|format(suma_total) }}</h2>
                <p>Suma Total</p>
            </div>
        </div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Valor</th>
                    <th>Fecha</th>
                    <th>Imagen</th>
                </tr>
            </thead>
            <tbody>
                {% for factura in facturas %}
                <tr>
                    <td>{{ factura.id }}</td>
                    <td>${{ "%.2f"|format(factura.valor) }}</td>
                    <td>{{ factura.fecha }}</td>
                    <td>
                        <a href="/{{ factura.imagen_path }}" target="_blank" class="btn btn-info" style="padding: 5px 10px; font-size: 12px;">Ver</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
""" + HTML_FOOTER


# ==================== RUTAS PRINCIPALES ====================
@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with get_db() as conn:
            user = conn.execute(
                "SELECT * FROM usuarios WHERE username = ? AND password = ?",
                (username, password),
            ).fetchone()

            if user:
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["rol"] = user["rol"]
                session["contador_id"] = user["contador_id"]
                return redirect(url_for("dashboard"))
            return render_template_string(LOGIN_TEMPLATE, error="Credenciales inválidas")

    return render_template_string(LOGIN_TEMPLATE, error=None)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required()
def dashboard():
    rol = session["rol"]

    if rol == "super_admin":
        return redirect(url_for("panel_super_admin"))
    if rol == "contador":
        return redirect(url_for("panel_contador"))
    if rol == "cliente":
        return redirect(url_for("panel_cliente"))

    return redirect(url_for("logout"))


@app.route("/panel/super-admin")
@login_required(roles=["super_admin"])
def panel_super_admin():
    config = get_config()
    with get_db() as conn:
        contadores = conn.execute(
            "SELECT id, username, fecha_registro FROM usuarios WHERE rol = 'contador'"
        ).fetchall()
        clientes = conn.execute(
            "SELECT u.id, u.username, u.fecha_registro, c.username as contador "
            "FROM usuarios u LEFT JOIN usuarios c ON u.contador_id = c.id "
            "WHERE u.rol = 'cliente'"
        ).fetchall()

    return render_template_string(
        SUPER_ADMIN_TEMPLATE,
        config=config,
        contadores=contadores,
        clientes=clientes,
    )


@app.route("/panel/contador")
@login_required(roles=["contador"])
def panel_contador():
    fecha_inicio = request.args.get("fecha_inicio", "")
    fecha_fin = request.args.get("fecha_fin", "")

    with get_db() as conn:
        clientes = conn.execute(
            "SELECT id, username FROM usuarios WHERE contador_id = ? AND rol = 'cliente'",
            (session["user_id"],),
        ).fetchall()

        query = """
            SELECT f.*, u.username as cliente_nombre
            FROM facturas f
            JOIN usuarios u ON f.cliente_id = u.id
            WHERE u.contador_id = ?
        """
        params = [session["user_id"]]

        if fecha_inicio:
            query += " AND DATE(f.fecha) >= ?"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND DATE(f.fecha) <= ?"
            params.append(fecha_fin)

        query += " ORDER BY f.fecha DESC"
        facturas = conn.execute(query, params).fetchall()

        suma_total = sum(f["valor"] for f in facturas)

    return render_template_string(
        CONTADOR_TEMPLATE,
        clientes=clientes,
        facturas=facturas,
        suma_total=suma_total,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )


@app.route("/panel/cliente")
@login_required(roles=["cliente"])
def panel_cliente():
    with get_db() as conn:
        facturas = conn.execute(
            "SELECT * FROM facturas WHERE cliente_id = ? ORDER BY fecha DESC",
            (session["user_id"],),
        ).fetchall()

        suma_total = sum(f["valor"] for f in facturas)

    return render_template_string(
        CLIENTE_TEMPLATE,
        facturas=facturas,
        suma_total=suma_total,
    )


# ==================== RUTAS DE GESTIÓN ====================
@app.route("/crear-contador", methods=["POST"])
@login_required(roles=["super_admin"])
def crear_contador():
    username = request.form["username"]
    password = request.form["password"]

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, 'contador')",
                (username, password),
            )
        return redirect(url_for("panel_super_admin"))
    except sqlite3.IntegrityError:
        return "El usuario ya existe", 400


@app.route("/crear-cliente", methods=["POST"])
@login_required(roles=["contador"])
def crear_cliente():
    username = request.form["username"]
    password = request.form["password"]

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO usuarios (username, password, rol, contador_id) VALUES (?, ?, 'cliente', ?)",
                (username, password, session["user_id"]),
            )
        return redirect(url_for("panel_contador"))
    except sqlite3.IntegrityError:
        return "El usuario ya existe", 400


@app.route("/configuracion", methods=["POST"])
@login_required(roles=["super_admin"])
def actualizar_configuracion():
    contacto = request.form.get("contacto", "")
    privacidad = request.form.get("privacidad", "")
    info_general = request.form.get("info_general", "")
    precio_mensual = float(request.form.get("precio_mensual", 0))
    precio_semestral = float(request.form.get("precio_semestral", 0))
    precio_anual = float(request.form.get("precio_anual", 0))

    with get_db() as conn:
        conn.execute(
            """
            UPDATE configuracion
            SET contacto = ?, privacidad = ?, info_general = ?,
                precio_mensual = ?, precio_semestral = ?, precio_anual = ?
            WHERE id = 1
        """,
            (
                contacto,
                privacidad,
                info_general,
                precio_mensual,
                precio_semestral,
                precio_anual,
            ),
        )

    return redirect(url_for("panel_super_admin"))


@app.route("/subir-factura", methods=["POST"])
@login_required(roles=["cliente"])
def subir_factura():
    if "imagen" not in request.files:
        return "No se seleccionó imagen", 400

    file = request.files["imagen"]
    valor = request.form.get("valor", 0)

    if file.filename == "":
        return "No se seleccionó archivo", 400

    if file and file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        fecha_actual = datetime.now()
        user_folder = f"user_{session['user_id']}"
        fecha_folder = fecha_actual.strftime("%Y/%m")
        upload_path = os.path.join(UPLOAD_FOLDER, user_folder, fecha_folder)
        os.makedirs(upload_path, exist_ok=True)

        filename = secure_filename(f"{fecha_actual.strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        filepath = os.path.join(upload_path, filename)
        file.save(filepath)

        with get_db() as conn:
            conn.execute(
                "INSERT INTO facturas (cliente_id, imagen_path, valor) VALUES (?, ?, ?)",
                (session["user_id"], filepath, float(valor)),
            )

        return redirect(url_for("panel_cliente"))

    return "Formato de archivo no permitido", 400


@app.route("/descargar-facturas-zip")
@login_required(roles=["contador"])
def descargar_facturas_zip():
    fecha_inicio = request.args.get("fecha_inicio", "")
    fecha_fin = request.args.get("fecha_fin", "")

    with get_db() as conn:
        query = """
            SELECT f.* FROM facturas f
            JOIN usuarios u ON f.cliente_id = u.id
            WHERE u.contador_id = ?
        """
        params = [session["user_id"]]

        if fecha_inicio:
            query += " AND DATE(f.fecha) >= ?"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND DATE(f.fecha) <= ?"
            params.append(fecha_fin)

        facturas = conn.execute(query, params).fetchall()

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for factura in facturas:
            if os.path.exists(factura["imagen_path"]):
                fecha = factura["fecha"].split()[0]
                arcname = f"{fecha}/{os.path.basename(factura['imagen_path'])}"
                zf.write(factura["imagen_path"], arcname)

    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype="application/zip",
        as_attachment=True,
        download_name="facturas_organizadas.zip",
    )


# ==================== INICIAR APLICACIÓN ====================
if __name__ == "__main__":
    init_db()
    print("✅ Servidor iniciado en http://localhost:5000")
    print("👤 Usuario Admin: admin / admin123")
    app.run(debug=True, host="0.0.0.0", port=5000)
