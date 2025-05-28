from flask import Flask, request, jsonify, redirect, render_template
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# Estado de la chicharra
estado_buzzer = {"activo": True}

# Lista de pulsaciones (quién apretó y a qué hora)
pulsaciones = []

# Puntaje por mesa
puntos = defaultdict(int)

# Jugadores registrados con su mesa
jugadores = {}

# Clave para acceder como host
CLAVE_HOST = "123"

@app.route("/")
def index():
    return render_template("index.html")  # Asegúrate de tener templates/index.html

@app.route("/buzz", methods=["POST"])
def buzz():
    if not estado_buzzer["activo"]:
        return redirect("/")

    nombre = request.form["nombre"]
    if nombre not in [p["nombre"] for p in pulsaciones]:
        hora = datetime.now().strftime("%H:%M:%S")
        pulsaciones.append({"nombre": nombre, "hora": hora})
    return redirect("/")

@app.route("/estado")
def estado():
    return jsonify(pulsaciones)

@app.route("/puntos")
def puntos_estado():
    return jsonify(dict(puntos))

@app.route("/buzzer_estado")
def buzzer_estado():
    return jsonify(estado_buzzer)

@app.route("/toggle", methods=["POST"])
def toggle():
    clave = request.form.get("clave")
    if clave != CLAVE_HOST:
        return "Acceso denegado", 403
    estado_buzzer["activo"] = not estado_buzzer["activo"]
    return redirect("/")

@app.route("/reset", methods=["POST"])
def reset():
    clave = request.form.get("clave")
    if clave != CLAVE_HOST:
        return "Acceso denegado", 403
    if estado_buzzer["activo"]:
        pulsaciones.clear()
    return redirect("/")

@app.route("/sumar", methods=["POST"])
def sumar():
    clave = request.form.get("clave")
    if clave != CLAVE_HOST:
        return "Acceso denegado", 403

    jugador = request.form.get("jugador")
    mesa = jugadores.get(jugador)

    if mesa:
        puntos[mesa] += 1

    return redirect("/")

@app.route("/guardar_jugador", methods=["POST"])
def guardar_jugador():
    data = request.get_json()
    nombre = data["nombre"]
    mesa = data["mesa"]
    jugadores[nombre] = mesa
    return "", 204

@app.route("/jugadores")
def jugadores_registrados():
    return jsonify(jugadores)

if __name__ == "__main__":
    app.run(debug=True)








