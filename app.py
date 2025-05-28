from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

clicks = []
usuarios = {}  # jugador → mesa
puntos = {}     # mesa → puntos
buzzer_activo = True
CLAVE_HOST = "Karina123"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buzz", methods=["POST"])
def buzz():
    global clicks
    if not buzzer_activo:
        return redirect(url_for("index"))

    nombre = request.form.get("nombre")
    if not nombre:
        return redirect(url_for("index"))

    if nombre not in [c['nombre'] for c in clicks]:
        clicks.append({
            "nombre": nombre,
            "hora": datetime.now().strftime("%H:%M:%S")
        })
        if nombre not in usuarios:
            if "(" in nombre and ")" in nombre:
                mesa = nombre.split("(")[-1].replace(")", "").strip()
                usuarios[nombre] = mesa
                puntos.setdefault(mesa, 0)

    return redirect(url_for("index"))

@app.route("/estado")
def estado():
    return jsonify(clicks)

@app.route("/puntos")
def ver_puntos():
    return jsonify(puntos)

@app.route("/jugadores")
def jugadores():
    return jsonify(usuarios)

@app.route("/sumar", methods=["POST"])
def sumar():
    clave = request.form.get("clave")
    jugador = request.form.get("jugador")

    if clave == CLAVE_HOST and jugador in usuarios:
        mesa = usuarios[jugador]
        puntos[mesa] = puntos.get(mesa, 0) + 1

    return redirect(url_for("index"))

@app.route("/reset", methods=["POST"])
def reset():
    global clicks
    clave = request.form.get("clave")
    if clave == CLAVE_HOST:
        clicks = []
    return redirect(url_for("index"))

@app.route("/toggle", methods=["POST"])
def toggle():
    global buzzer_activo
    clave = request.form.get("clave")
    if clave == CLAVE_HOST:
        buzzer_activo = not buzzer_activo
    return redirect(url_for("index"))

@app.route("/buzzer_estado")
def buzzer_estado():
    return jsonify({"activo": buzzer_activo})

if __name__ == "__main__":
    app.run(debug=True)






