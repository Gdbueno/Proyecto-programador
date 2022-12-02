from flask import Flask, render_template, request, jsonify, Response, redirect, url_for, flash
import traceback
import datetime
from flask_sqlalchemy import SQLAlchemy

from equipos import maquinas


import grafico

import equipos

db = SQLAlchemy
app = Flask(__name__)
# Crear sesion flash
app.secret_key = "secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///equipos.db"
equipos.db.init_app(app)

# Funcion para que se cree la DB al inicio de la app


@app.before_first_request
def before_first_request_func():
    equipos.db.create_all()

# Principal


@app.route('/')
def inicio():
    try:
        return render_template('index.html')
    except:
        return jsonify({'trace': traceback.format_exc()})

# Lista


@app.route('/tabla')
def tabla():
    try:
        datos = maquinas.query.all()
        return render_template('tabla.html', datos=datos)
    except:
        return jsonify({'trace': traceback.format_exc()})

# Nuevo registro


@app.route('/nuevo', methods=['POST'])
def registro():
    try:
        horario = datetime.datetime.now()
        equipo = request.form['equipo']
        tarea = request.form['tarea']
        operario = request.form['operario']
        hstrab = request.form['hstrabajadas']
        nuevo_registro = maquinas(horario, equipo, tarea, operario, hstrab)
        equipos.db.session.add(nuevo_registro)
        equipos.db.session.commit()
        flash("Registro añadido")
        return redirect(url_for('tabla'))
    except:
        return jsonify({'trace': traceback.format_exc()})

# Actualizar registro


@app.route('/actualizar/<id>', methods=['POST', 'GET'])
def actualizar(id):
    actualizar_dato = maquinas.query.get(id)
    if request.method == 'POST':
        try:
            actualizar_dato.horario = datetime.datetime.now()
            actualizar_dato.equipo = request.form['equipo']
            actualizar_dato.tarea = request.form['tarea']
            actualizar_dato.operario = request.form['operario']
            actualizar_dato.hs_trabajadas = request.form['hstrabajadas']

            equipos.db.session.commit()
            flash("Registro actualizado")
            return redirect(url_for('tabla'))
        except:
            return jsonify({'trace': traceback.format_exc()})

    return render_template('actualizar.html', dato=actualizar_dato)

# Borrar registro


@app.route('/borrar/<id>')
def borrar(id):
    try:
        borrar_dato = maquinas.query.get(id)
        equipos.db.session.delete(borrar_dato)
        equipos.db.session.commit()
        flash("Registro borrado")
        return redirect(url_for('tabla'))
    except:
        return jsonify({'trace': traceback.format_exc()})

# Grafico


@app.route('/graficos', methods=['GET', 'POST'])
def graficos():
    if request.method == 'GET':
        try:
            return render_template('grafico.html')
        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        try:

            equipo = ""

            equipo = str(request.form.get('equipos'))

            x, y = equipos.datos_grafica(equipo)

            eje_x = 'Horario/equipo', equipo
            eje_y = 'Hs Trabajadas'
            titulo = 'Horas trabajadas por equipo'

            image_html = grafico.graficar(x, y, eje_x, eje_y, titulo)

            return Response(image_html.getvalue(), mimetype='image/png')
        except:
            return jsonify({'trace': traceback.format_exc()})

# Info


@app.route('/info')
def info():
    return render_template('info.html')


if __name__ == "__main__":
    app.run(debug=True)
