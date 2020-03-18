from application import app, db
from flask import render_template, request, redirect, url_for
from application.plants.models import Plant

@app.route("/plants/", methods=["GET"])
def plants_index():
    return render_template("plants/list.html", plants = Plant.query.all())


@app.route("/plants/new/")
def plants_form():
    return render_template("plants/new.html")

@app.route("/plants/<plant_id>/")
def plants_update_form(plant_id):
    return render_template("plants/update.html", plant_id = plant_id, vanha = Plant.query.get(plant_id))

@app.route("/plants/<plant_id>/", methods=["POST"])
def plants_update(plant_id):

    p = Plant.query.get(plant_id)
    p.nimi = request.form.get("nimi_uusi")
    p.nimi_lat = request.form.get("nimi_lat_uusi")
    db.session().commit()

    return redirect(url_for("plants_index"))


@app.route("/plants/new/", methods=["POST"])
def plants_create():

    nimi = request.form.get("nimi")
    nimi_lat = request.form.get("nimi_lat")
    vedentarve = request.form.get("vedentarve")
    lannoituksentarve = request.form.get("lannoituksentarve")
    valontarve = request.form.get("valontarve")

    p = Plant(nimi, nimi_lat, vedentarve, lannoituksentarve, valontarve)

    db.session().add(p)
    db.session().commit()

    return redirect(url_for("plants_index"))
