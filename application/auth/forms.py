from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):

    username = StringField("Käyttäjänimi")
    password = PasswordField("Salasana")

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):

    username = StringField("Käyttäjänimi", [validators.Length(min = 2, message = "Käyttäjänimen tulee olla vähintään 2 merkkiä pitkä")])
    password = PasswordField("Salasana", [validators.Length(min = 2, message = "Salasanan tulee olla vähintään 2 merkkiä pitkä")])

    class Meta:
        csrf = False
