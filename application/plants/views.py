from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required
from application.plants.models import Plant, PlantUser, Category, PlantCategory
from application.plants.forms import PlantForm, SearchPlantForm, CategoryForm, SearchCategoryForm, UpdateLastWateredForm, UpdateLastFertilizedForm
from application.auth.models import User

from sqlalchemy.sql import text

@app.route("/show/user", methods = ["GET"])
@login_required()
def plants_show_user():

    result = PlantUser.user_plants(current_user.id)

    number = Plant.user_plants_number(current_user.id)

    #replace id of plant with plant object, format the dates
    for sublist in result:
        sublist[0] = Plant.query.get(sublist[0])

        if sublist[1] != None:
            print("--------")
            print(sublist[1])
            sublist[1] = str(sublist[1])
            print(sublist[1])
            newformat_split_w = sublist[1].split("-")
            newformat_w = newformat_split_w[2] + "." + newformat_split_w[1] + "." + newformat_split_w[0]
            sublist[1] = newformat_w
        else:
            sublist[1] = "Ei valittua päivää"

        if sublist[2] != None:
            print("--------")
            print(sublist[2])
            sublist[2] = str(sublist[2])
            print(sublist[2])
            newformat_split_f = sublist[2].split("-")
            newformat_f = newformat_split_f[2] + "." + newformat_split_f[1] + "." + newformat_split_f[0]
            sublist[2] = newformat_f
        else:
            sublist[2] = "Ei valittua päivää"

    return render_template("plants/listuser.html", plants = result, lastwateredform = UpdateLastWateredForm(), lastfertilizedform = UpdateLastFertilizedForm(), number = number)

@app.route("/show/all")
def plants_show_all():

    allPlants = Plant.query.all()
    number = Plant.all_plants_number()

    return render_template("plants/listall.html", plants = allPlants, searchplantform = SearchPlantForm(), searchcategoryform = SearchCategoryForm(), number = number)


@app.route("/new/plant")
@login_required(role = "ADMIN")
def plants_new_form():

    return render_template("plants/new.html", form = PlantForm())

@app.route("/new/plant", methods = ["POST"])
@login_required(role = "ADMIN")
def plants_new():

    form = PlantForm(request.form)

    if not form.validate():
        return render_template("plants/new.html", form = form)

    nameExists = Plant.query.filter_by(name_fin = form.name_fin.data).first()
    if nameExists:
        return render_template("plants/new.html", form = form, error = "Kasvi löytyy jo tietokannasta!")

    name_fin = form.name_fin.data
    name_lat = form.name_lat.data
    water_need = form.water_need.data
    fertilizer_need = form.fertilizer_need.data
    light_need = form.light_need.data

    p = Plant(name_fin, name_lat, water_need, fertilizer_need, light_need)

    db.session().add(p)
    db.session().commit()

    return redirect(url_for("plants_show_all"))

@app.route("/update/plant/<plant_id>/")
@login_required(role = "ADMIN")
def plants_update_form(plant_id):

    p = Plant.query.get(plant_id)
    return render_template("plants/update.html", plant_id = plant_id, form = PlantForm(obj = p))

@app.route("/update/plant/<plant_id>/", methods = ["POST"])
@login_required(role = "ADMIN")
def plants_update(plant_id):

    p = Plant.query.get(plant_id)
    form = PlantForm(request.form)

    if not form.validate():
        return render_template("plants/update.html", plant_id = plant_id, form = form)

    p.name_fin = form.name_fin.data
    p.name_lat = form.name_lat.data
    p.water_need = form.water_need.data
    p.fertilizer_need = form.fertilizer_need.data
    p.light_need = form.light_need.data

    db.session().commit()

    return redirect(url_for("plants_show_all"))

@app.route("/delete/plant/<plant_id>", methods = ["POST"])
@login_required(role = "ADMIN")
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

@app.route("/new/user/connection/<plant_id>", methods = ["POST"])
@login_required
def plants_new_user_connection(plant_id):

    p = Plant.query.get(plant_id)
    user = User.query.get(current_user.id)

    connectionExists = PlantUser.query.filter_by(user = user, plant = p).first()
    if not connectionExists:
        pu = PlantUser(plant = p, user = user)

        db.session().add(pu)
        db.session().commit()

    return redirect(url_for("plants_show_all"))

@app.route("/delete/user/connection/<plant_id>", methods = ["POST"])
@login_required
def plants_delete_user_connection(plant_id):

    p = Plant.query.get(plant_id)
    pu = PlantUser.query.filter_by(user = current_user, plant = p).first()
    db.session.delete(pu)
    db.session.commit()

    return redirect(url_for("plants_show_user"))

@app.route("/search/name", methods = ["POST"])
def plants_search():

    form = SearchPlantForm(request.form)

    name_fin = form.name_fin.data

    result = Plant.find_plant_by_name(name_fin = name_fin)

    allPlants = Plant.query.all()
    number = Plant.all_plants_number()

    if not result:
        return render_template("plants/listall.html", plants = allPlants, searchplantform = SearchPlantForm(), searchcategoryform = SearchCategoryForm(),  noresult_plant = True, number = number)

    results = []
    p = Plant(result[1], result[2], result[3], result[4], result[5])
    p.id = result[0]
    results.append(p)

    return render_template("plants/searchresults.html", plants = results, header = "Tulokset haulla " + name_fin, number = 1)

@app.route("/search/category", methods = ["POST"])
def categories_search():

    form = SearchCategoryForm(request.form)

    if not form.validate():
        return render_template("plants/listall.html", searchcategoryform = form)

    c_data = form.category.data
    c_plants = []

    allPlants = Plant.query.all()
    number = Plant.all_plants_number()

    allInstances = PlantCategory.query.all()
    for i in allInstances:
        if i.category_id is int(c_data.id):
            p = Plant.query.get(i.plant_id)
            c_plants.append(p)

    if len(c_plants) == 0:
        return render_template("plants/listall.html", plants = allPlants, searchplantform = SearchPlantForm(), searchcategoryform = SearchCategoryForm(), noresult_category = True, number = number)

    return render_template("plants/searchresults.html", plants = c_plants, header = "Kategorian " + c_data.name + " kasvit", number = len(c_plants))

@app.route("/new/category/", methods = ["GET"])
@login_required(role = "ADMIN")
def categories_new_form():

    number = Category.categories_number()

    return render_template("categories/new.html", form = CategoryForm(), categories = Category.query.all(), number = number)

@app.route("/new/category/", methods = ["POST"])
@login_required(role = "ADMIN")
def categories_new():

    form = CategoryForm(request.form)

    if not form.validate():
        return render_template("categories/new.html", form = form, categories = Category.query.all())

    categoryExists = Category.query.filter_by(name = form.name.data).first()
    if categoryExists:
        return render_template("categories/new.html", form = form, error = "Tämän niminen kategoria on jo olemassa!", categories = Category.query.all())

    name = form.name.data
    description = form.description.data

    c = Category(name, description)

    db.session().add(c)
    db.session().commit()

    return redirect(url_for("categories_new"))

@app.route("/new/category/connection/<category_id>/<plant_id>")
@login_required(role = "ADMIN")
def categories_new_plant_connection(category_id, plant_id):

    p = Plant.query.get(plant_id)
    c = Category.query.get(category_id)

    connectionExists = PlantCategory.query.filter_by(plant = p, category = c).first()
    if not connectionExists:
        pc = PlantCategory(plant = p, category = c)

        db.session().add(pc)
        db.session().commit()

    return redirect(url_for("categories_manage_one", category_id = category_id))

@app.route("/delete/category/connection/<category_id>/<plant_id>")
@login_required(role = "ADMIN")
def categories_delete_plant_connection(category_id, plant_id):

    p = Plant.query.get(plant_id)
    c = Category.query.get(category_id)
    pc = PlantCategory.query.filter_by(plant = p, category = c).first()
    db.session.delete(pc)
    db.session.commit()

    return redirect(url_for("categories_manage_one", category_id = category_id))

@app.route("/manage/categories/", methods = ["GET"])
@login_required(role = "ADMIN")
def categories_manage_all():

    number = Category.categories_number()

    return render_template("/categories/manageall.html", categories = Category.query.all(), number = number)

@app.route("/manage/categories/update/<category_id>", methods = ["GET"])
@login_required(role = "ADMIN")
def categories_update_form(category_id):

    c = Category.query.get(category_id)
    return render_template("/categories/update.html", category_id = category_id, form = CategoryForm(obj=c))

@app.route("/manage/categories/update/<category_id>", methods = ["POST"])
@login_required(role = "ADMIN")
def categories_update(category_id):

    c = Category.query.get(category_id)
    form = CategoryForm(request.form)

    if not form.validate():
        return render_template("categories/update.html", category_id = category_id, form = form)

    c.name = form.name.data
    c.description = form.description.data

    db.session().commit()

    return redirect(url_for("categories_manage_all"))

@app.route("/manage/categories/<category_id>", methods = ["GET"])
@login_required(role = "ADMIN")
def categories_manage_one(category_id):

    c = Category.query.get(category_id)

    number_one = Category.category_plants_number(category_id)
    number_all = Plant.all_plants_number()

    c_plants = []
    allPlants = Plant.query.all()

    allInstances = PlantCategory.query.all()
    for i in allInstances:
        if i.category_id is int(category_id):
            p = Plant.query.get(i.plant_id)
            c_plants.append(p)

    return render_template("/categories/manageone.html", category_id = c.id, name = c.name, c_plants = c_plants, plants = allPlants, number_one = number_one, number_all = number_all)

@app.route("/manage/categories/search/name", methods = ["POST"])
@login_required(role = "ADMIN")
def categories_search_plant():

    form = SearchPlantForm(request.form)

    if not form.validate():
        return render_template("categories/manageall.html", form = form)

    name_fin = form.name_fin.data

    result = Plant.find_plant_by_name(name_fin = name_fin)

    if not result:
        return render_template("plants/noresults.html")

    results = []
    p = Plant(result[1], result[2], result[3], result[4], result[5])
    results.append(p)

    return render_template("categories/searchresults.html", plants = results, plant_id = result[0])

@app.route("/manage/categories/delete/<category_id>")
@login_required(role = "ADMIN")
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

@app.route("/update/plantuser/lastwatered/<plant_id>", methods = ["POST"])
@login_required()
def plants_update_last_watered(plant_id):

    form = UpdateLastWateredForm(request.form)

    plantuser = PlantUser.query.filter_by(plant_id = plant_id, user_id = current_user.id).first()
    plantuser.last_watered = form.newdate.data

    db.session.add(plantuser)
    db.session.commit()

    return redirect(url_for("plants_show_user"))

@app.route("/update/plantuser/lastfertilized/<plant_id>", methods = ["POST"])
@login_required()
def plants_update_last_fertilized(plant_id):

    form = UpdateLastFertilizedForm(request.form)

    plantuser = PlantUser.query.filter_by(plant_id = plant_id, user_id = current_user.id).first()
    plantuser.last_fertilized = form.newdate.data

    db.session.add(plantuser)
    db.session.commit()

    return redirect(url_for("plants_show_user"))
