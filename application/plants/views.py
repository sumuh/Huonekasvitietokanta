from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.plants.models import Plant, PlantUser, Category, PlantCategory
from application.plants.forms import PlantForm, SearchForm, CategoryForm, SearchCategoryForm
from application.auth.models import User

from sqlalchemy.sql import text

@app.route("/show/user", methods=["GET"])
@login_required
def plants_show_user():
    #userPlants = []

    #allInstances = PlantUser.query.all()
    #for i in allInstances:
    #    if i.user_id == current_user.id:
    #        p = Plant.query.get(i.plant_id)
    #        userPlants.append(p)

    result = PlantUser.user_plants(current_user.id)
    results = []

    for r in result:
        p = Plant.query.get(r)
        results.append(p)

    return render_template("plants/listuser.html", plants = results)

@app.route("/show/all")
def plants_show_all():
    allPlants = Plant.query.all()
    return render_template("plants/listall.html", plants = allPlants, searchform = SearchForm(), searchcategoryform = SearchCategoryForm())


@app.route("/new/plant")
@login_required
def plants_new_form():
    return render_template("plants/new.html", form = PlantForm())

@app.route("/new/plant", methods=["POST"])
@login_required
def plants_new():

    form = PlantForm(request.form)

    if not form.validate():
        return render_template("plants/new.html", form = form)

    nameExists = Plant.query.filter_by(nimi=form.nimi.data).first()
    if nameExists:
        return render_template("plants/new.html", form = form, error = "Kasvi löytyy jo tietokannasta!")

    nimi = form.nimi.data
    nimi_lat = form.nimi_lat.data
    vedentarve = form.vedentarve.data
    lannoituksentarve = form.lannoituksentarve.data
    valontarve = form.valontarve.data

    p = Plant(nimi, nimi_lat, vedentarve, lannoituksentarve, valontarve)

    db.session().add(p)
    db.session().commit()

    return redirect(url_for("plants_show_all"))

@app.route("/update/plant/<plant_id>/")
@login_required
def plants_update_form(plant_id):
    p = Plant.query.get(plant_id)
    return render_template("plants/update.html", plant_id = plant_id, form = PlantForm(obj=p))

@app.route("/update/plant/<plant_id>/", methods=["POST"])
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

@app.route("/delete/plant/<plant_id>", methods=['POST'])
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

@app.route("/new/user/connection/<plant_id>", methods=["POST"])
@login_required
def plants_new_user_connection(plant_id):

    p = Plant.query.get(plant_id)
    user = User.query.get(current_user.id)

    connectionExists = PlantUser.query.filter_by(user=user, plant=p).first()
    if not connectionExists:
        pu = PlantUser(plant=p, user=user)

        db.session().add(pu)
        db.session().commit()

    return redirect(url_for("plants_show_all"))

@app.route("/delete/user/connection/<plant_id>", methods=['POST'])
@login_required
def plants_delete_user_connection(plant_id):

    p = Plant.query.get(plant_id)
    pu = PlantUser.query.filter_by(user=current_user, plant=p).first()
    db.session.delete(pu)
    db.session.commit()

    return redirect(url_for("plants_show_user"))

@app.route("/search/name", methods=['POST'])
def plants_search():

    searchform = SearchForm(request.form)

    if not searchform.validate():
        return render_template("plants/listall.html", searchform = searchform)

    nimi = searchform.nimi.data

    result = Plant.find_plant_by_name(name=nimi)

    if not result:
        return render_template("plants/noresults.html", text = "Haulla ei löytynyt kasveja!")

    results = []
    p = Plant(result[1], result[2], result[3], result[4], result[5])
    results.append(p)

    return render_template("plants/searchresults.html", plants = results, plant_id = result[0], header = "Tulokset haulla " + nimi)

@app.route("/search/category", methods=['POST'])
def categories_search():

    searchcategoryform = SearchCategoryForm(request.form)

    if not searchcategoryform.validate():
        return render_template("plants/listall.html", searchcategoryform = searchcategoryform)

    c_data = searchcategoryform.kategoria.data

    c_plants = []

    allInstances = PlantCategory.query.all()
    for i in allInstances:
        if i.category_id is int(c_data.id):
            p = Plant.query.get(i.plant_id)
            c_plants.append(p)

    if len(c_plants) is 0:
        return render_template("plants/noresults.html", text = "Kategoriassa ei ole kasveja!")

    return render_template("plants/searchresults.html", plants = c_plants, header = "Kategorian " + c_data.nimi + " kasvit")

@app.route("/new/category/", methods=['GET'])
@login_required
def categories_new_form():
    return render_template("categories/new.html", form = CategoryForm(), kategoriat=Category.query.all())

@app.route("/new/category/", methods=['POST'])
def categories_new():

    form = CategoryForm(request.form)

    if not form.validate():
        return render_template("categories/new.html", form = form, kategoriat=Category.query.all())

    categoryExists = Category.query.filter_by(nimi=form.nimi.data).first()
    if categoryExists:
        return render_template("categories/new.html", form = form, error = "Tämän niminen kategoria on jo olemassa!", kategoriat=Category.query.all())

    nimi = form.nimi.data
    kuvaus = form.kuvaus.data

    c = Category(nimi, kuvaus)

    db.session().add(c)
    db.session().commit()

    return redirect(url_for("categories_new"))

@app.route("/new/category/connection/<category_id>/<plant_id>")
@login_required
def categories_new_plant_connection(category_id, plant_id):

    p = Plant.query.get(plant_id)
    c = Category.query.get(category_id)

    connectionExists = PlantCategory.query.filter_by(plant=p, category=c).first()
    if not connectionExists:
        pc = PlantCategory(plant=p, category=c)

        db.session().add(pc)
        db.session().commit()

    return redirect(url_for("categories_manage_one", category_id = category_id))

@app.route("/delete/category/connection/<category_id>/<plant_id>")
@login_required
def categories_delete_plant_connection(category_id, plant_id):

    p = Plant.query.get(plant_id)
    c = Category.query.get(category_id)
    pc = PlantCategory.query.filter_by(plant=p, category=c).first()
    db.session.delete(pc)
    db.session.commit()

    return redirect(url_for("categories_manage_one", category_id=category_id))

@app.route("/manage/categories/", methods=['GET'])
@login_required
def categories_manage_all():
    return render_template("/categories/manageall.html", kategoriat=Category.query.all())

@app.route("/manage/categories/update/<category_id>", methods=['GET'])
@login_required
def categories_update_form(category_id):
    c = Category.query.get(category_id)
    return render_template("/categories/update.html", category_id = category_id, form = CategoryForm(obj=c))

@app.route("/manage/categories/update/<category_id>", methods=['POST'])
@login_required
def categories_update(category_id):

    c = Category.query.get(category_id)
    form = CategoryForm(request.form)

    if not form.validate():
        return render_template("categories/update.html", category_id = plant_id, form = form)

    c.nimi = form.nimi.data
    c.kuvaus = form.kuvaus.data

    db.session().commit()

    return redirect(url_for("categories_manage_all"))

@app.route("/manage/categories/<category_id>", methods=['GET'])
@login_required
def categories_manage_one(category_id):
    c = Category.query.get(category_id)

    c_plants = []
    allPlants = Plant.query.all()

    allInstances = PlantCategory.query.all()
    for i in allInstances:
        if i.category_id is int(category_id):
            p = Plant.query.get(i.plant_id)
            c_plants.append(p)

    return render_template("/categories/manageone.html", category_id = c.id, nimi = c.nimi, c_plants = c_plants, plants=allPlants)

@app.route("/manage/categories/search/name", methods=['POST'])
def categories_search_plant():

    searchform = SearchForm(request.form)

    if not searchform.validate():
        return render_template("categories/manageall.html", searchform = searchform)

    nimi = searchform.nimi.data

    result = Plant.find_plant_by_name(name=nimi)

    if not result:
        return render_template("plants/noresults.html")

    results = []
    p = Plant(result[1], result[2], result[3], result[4], result[5])
    results.append(p)

    return render_template("categories/searchresults.html", plants = results, plant_id = result[0])

@app.route("/manage/categories/delete/<category_id>")
@login_required
def categories_delete(category_id):

    c = Category.query.get(category_id)
    pc = PlantCategory.query.all()
    for i in pc:
        if i.category_id == category_id:
            db.session.delete(i)
            db.session.commit()

    db.session.delete(c)
    db.session.commit()

    return redirect(url_for("categories_manage_all"))
