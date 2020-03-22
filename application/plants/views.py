from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.plants.models import Plant
from application.plants.forms import PlantForm

@app.route("/plants/", methods=["GET"])
def plants_index():
    return render_template("plants/list.html", plants = Plant.query.all())


@app.route("/plants/new/")
@login_required
def plants_form():
    return render_template("plants/new.html", form = PlantForm())

@app.route("/plants/<plant_id>/")
@login_required
def plants_update_form(plant_id):
    p = Plant.query.get(plant_id)
    return render_template("plants/update.html", plant_id = plant_id, form = PlantForm(obj=p))

@app.route("/plants/<plant_id>/", methods=["POST"])
@login_required
def plants_update(plant_id):

    p = Plant.query.get(plant_id)
    form = PlantForm(request.form)

    if not form.validate():
        return render_template("plants/update.html", plant_id = plant_id, form = form)

    p.nimi = form.nimi.data
    p.nimi_lat = form.nimi_lat.data
    p.vedentarve = form.vedentarve.data
    p.lannoituksentarve = form.lannoituksentarve.data
    p.valontarve = form.valontarve.data

    db.session().commit()

    return redirect(url_for("plants_index"))


@app.route("/plants/new/", methods=["POST"])
@login_required
def plants_create():

    form = PlantForm(request.form)

    if not form.validate():
        return render_template("plants/new.html", form = form)

    nimi = form.nimi.data
    nimi_lat = form.nimi_lat.data
    vedentarve = form.vedentarve.data
    lannoituksentarve = form.lannoituksentarve.data
    valontarve = form.valontarve.data

    p = Plant(nimi, nimi_lat, vedentarve, lannoituksentarve, valontarve)

    p.account_id = current_user.id

    db.session().add(p)
    db.session().commit()

    return redirect(url_for("plants_index"))
