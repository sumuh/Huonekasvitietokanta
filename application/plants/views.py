from application import app, db
from flask import render_template, request
from application.plants.models import Plant

@app.route("/plants/new/")
def plants_form():
    return render_template("plants/new.html")

@app.route("/plants/", methods=["POST"])
def plants_create():

    nimi = request.form.get("nimi")
    nimi_lat = request.form.get("nimi_lat")
    vedentarve = request.form.get("vedentarve")
    lannoituksentarve = request.form.get("lannoituksentarve")
    valontarve = request.form.get("valontarve")

    p = Plant(nimi, nimi_lat, vedentarve, lannoituksentarve, valontarve)

    db.session().add(p)
    db.session().commit()

    return "hello world!"
