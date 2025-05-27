from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)
clicks = []
puntos = {}  # puntos por mesa
usuarios = {}  # usuario: mesa asociada

CLAVE_HOST = "miclave123"  # CAMBIA esta clave

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buzz", methods=["POST"])
def buzz():
    nombre = request.form.get("nombre")
    if nombre and nombre not in [c['nombre'] for c in clicks]:
        clicks.append({"nombre": nombre, "hora": datetime.now().strftime("%H:%M:%S")})

        # registrar mesa si es nueva
        if nombre not in usuarios:
            if "(" in nombre and ")" in nombre:
                mesa = nombre.split("(")[-1].replace(")", "").strip()
                usuarios[nombre] = mesa
                if mesa not in puntos:
                    puntos[mesa] = 0
    return redirect(url_for('index'))

@app.route("/reset", methods=["POST"])
def reset():
    clave = request.form.get("clave")
    if clave == CLAVE_HOST:
        clicks.clear()
    return redirect(url_for('index'))

@app.route("/estado")
def estado():
    return jsonify(clicks)

@app.route("/puntos")
def ver_puntos():
    return jsonify(puntos)

@app.route("/sumar", methods=["POST"])
def sumar_punto():
    clave = request.form.get("clave")
    jugador = request.form.get("jugador")
    if clave == CLAVE_HOST and jugador in usuarios:
        mesa = usuarios[jugador]
        puntos[mesa] = puntos.get(mesa, 0) + 1
    return redirect(url_for('index'))

@app.route("/jugadores")
def lista_jugadores():
    return jsonify(usuarios)

if __name__ == "__main__":
    app.run(debug=True)

