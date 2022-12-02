

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class maquinas(db.Model):
    __tablename__ = "Equipos"
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.DateTime)
    equipo = db.Column(db.String)
    tarea = db.Column(db.Integer)
    operario = db.Column(db.String)
    hs_trabajadas = db.Column(db.Integer)

    def __init__(self, horario, equipo, tarea, operario, hs_trabajadas):
        self.horario = horario
        self.equipo = equipo
        self.tarea = tarea
        self.operario = operario
        self.hs_trabajadas = hs_trabajadas


def datos_grafica(equipo):

    query = db.session.query(maquinas).filter(maquinas.tarea)
    query_results = query.all()
    print(query_results)

    if query_results is None or len(query_results) == 0:

        return []

    x = [x.horario for x in query_results if x.equipo == equipo]

    y = [x.hs_trabajadas for x in query_results if x.equipo == equipo]

    return x, y


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdatabase.db"

    db.init_app(app)
    app.app_context().push()
