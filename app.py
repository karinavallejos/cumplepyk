from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# Estado inicial
orden = []
puntos = defaultdict(int)
buzzer_activo = True
clave_host = "123"

# === Rutas ===
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buzz", methods=["POST"])
def buzz():
    nombre = request.form.get("nombre")
    if not buzzer_activo:
        return redirect("/")
    if nombre not in [item["nombre"] for item in orden]:
        orden.append({"nombre": nombre, "hora": datetime.now().strftime("%H:%M:%S")})
    return redirect("/")

@app.route("/estado")
def estado():
    return jsonify(orden)

@app.route("/puntos")
def puntos_totales():
    return jsonify(puntos)

@app.route("/reset", methods=["POST"])
def reset():
    if request.form.get("clave") != clave_host:
        return "", 403
    global orden
    orden = []
    return redirect("/")

@app.route("/toggle", methods=["POST"])
def toggle():
    if request.form.get("clave") != clave_host:
        return "", 403
    global buzzer_activo
    buzzer_activo = not buzzer_activo
    return redirect("/")

@app.route("/buzzer_estado")
def buzzer_estado():
    return jsonify({"activo": buzzer_activo})

@app.route("/sumar", methods=["POST"])
def sumar():
    if request.form.get("clave") != clave_host:
        return "", 403
    jugador = request.form.get("jugador")
    if jugador:
        mesa = jugador.split("(")[-1].replace(")", "").strip()
        puntos[mesa] += 1
    return redirect("/")

@app.route("/jugadores")
def jugadores():
    jugadores_lista = {item["nombre"]: 1 for item in orden}
    return jsonify(jugadores_lista)

if __name__ == "__main__":
    app.run(debug=True)


