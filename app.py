# -*- coding: utf-8 -*-
"""
Created on Mon May 26 22:40:29 2025

@author: kvallejos
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)
clicks = []  # almacena los clics en orden (nombre + hora)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buzz", methods=["POST"])
def buzz():
    nombre = request.form.get("nombre")
    if nombre and nombre not in [c['nombre'] for c in clicks]:
        clicks.append({"nombre": nombre, "hora": datetime.now().strftime("%H:%M:%S")})
    return redirect(url_for('index'))

@app.route("/reset")
def reset():
    clicks.clear()
    return redirect(url_for('index'))

@app.route("/estado")
def estado():
    return jsonify(clicks)

if __name__ == "__main__":
    app.run(debug=True)
