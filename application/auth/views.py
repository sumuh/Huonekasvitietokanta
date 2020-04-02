from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    if not form.validate():
        return render_template("auth/loginform.html", form = form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form, error = "Käyttäjänimi tai salasana on väärin")

    login_user(user)
    return redirect(url_for("plants_show_all"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/register.html", form = RegisterForm())

    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("auth/register.html", form = form)

    usernameExists = User.query.filter_by(username=form.username.data).first()
    if usernameExists:
        return render_template("auth/register.html", form = form, error = "Käyttäjänimi on jo käytössä")

    username = form.username.data
    password = form.password.data
    user = User(username, password)
    db.session.add(user)
    db.session.commit()

    return render_template("auth/registersuccess.html")
