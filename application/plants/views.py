from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.plants.models import Plant, PlantUser, Category, PlantCategory
from application.plants.forms import PlantForm, SearchForm, CreateCategoryForm, SearchCategoryForm
from application.auth.models import User

from sqlalchemy.sql import text

@app.route("/plants/", methods=["GET"])
@login_required
def plants_show_user():
    userPlants = []
    
    allInstances = PlantUser.query.all()
    for i in allInstances:
        if i.user_id == current_user.id:
            p = Plant.query.get(i.plant_id)
            userPlants.append(p)

    return render_template("plants/listuser.html", plants = userPlants)

@app.route("/plants/all/")
def plants_show_all():
    allPlants = Plant.query.all()
    return render_template("plants/listall.html", plants = allPlants, searchform = SearchForm(), searchcategoryform = SearchCategoryForm())


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

    return redirect(url_for("plants_show_all"))


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

    db.session().add(p)
    db.session().commit()

    return redirect(url_for("plants_show_all"))

@app.route("/plants/add/<plant_id>", methods=["POST"])
@login_required
def plants_add(plant_id):

    p = Plant.query.get(plant_id)
    user = User.query.get(current_user.id)

    connectionExists = PlantUser.query.filter_by(user=user, plant=p).first()
    if not connectionExists:
        pu = PlantUser(plant=p, user=user)

        db.session().add(pu)
        db.session().commit()

    return redirect(url_for("plants_show_all"))

@app.route("/plants/delete/<plant_id>", methods=['POST'])
@login_required
def plants_delete(plant_id):

    p = Plant.query.get(plant_id)
    pu = PlantUser.query.all()
    for i in pu:
        if i.plant_id == plant_id:
            db.session.delete(i)
            db.session.commit()

    db.session.delete(p)
    db.session.commit()

    return redirect(url_for("plants_show_all"))

@app.route("/plants/remove/<plant_id>", methods=['POST'])
@login_required
def plants_remove(plant_id):

    p = Plant.query.get(plant_id)
    pu = PlantUser.query.filter_by(user=current_user, plant=p).first()
    db.session.delete(pu)
    db.session.commit()

    return redirect(url_for("plants_show_user"))

@app.route("/plants/search/", methods=['POST'])
#@login_required
def plants_search():

    searchform = SearchForm(request.form)

    if not searchform.validate():
        return render_template("plants/listall.html", searchform = searchform)

    nimi = searchform.nimi.data

    result = Plant.find_plant_by_name(name=nimi)

    if not result:
        return render_template("plants/noresults.html")

    results = []
    p = Plant.query.get(result)
    results.append(p)

    return render_template("plants/searchresults.html", plants = results)

@app.route("/plants/search/category", methods=['POST'])
#@login_required
def plants_search_category():

    searchcategoryform = SearchCategoryForm(request.form)

    if not searchcategoryform.validate():
        return render_template("plants/listall.html", searchcategoryform = searchcategoryform)

    kategoria = searchcategoryform.kategoria.data

    result = Plant.find_plant_by_name(name=nimi)

    results = []
    p = Plant.query.get(result)
    results.append(p)

    return render_template("plants/searchresults.html", plants = results)

@app.route("/plants/newcategory/", methods=['GET'])
@login_required
def category_form():
    return render_template("categories/new.html", form = CreateCategoryForm(), kategoriat=Category.query.all())

@app.route("/plants/newcategory/", methods=['POST'])
def category_create():

    form = CreateCategoryForm(request.form)

    if not form.validate():
        return render_template("categories/new.html", form = form)

    nimi = form.nimi.data
    kuvaus = form.kuvaus.data

    exists = Category.query.filter_by(nimi=nimi).first()
    if not exists:
        c = Category(nimi, kuvaus)

        db.session().add(c)
        db.session().commit()

    return redirect(url_for("plants_show_all"))
