from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, validators, RadioField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from application.auth.models import User
from .models import Plant, PlantUser, Category, PlantCategory

class PlantForm(FlaskForm):
    nimi = StringField("Kasvin nimi", [validators.Length(min=2, message="Nimen tulee olla vähintään 2 merkkiä pitkä")])
    nimi_lat = StringField("Latinankielinen nimi", [validators.Length(min=2, message="Nimen tulee olla vähintään 2 merkkiä pitkä")])
    vedentarve = SelectField(
        "Vedentarve",
        choices=[('Pieni', 'Pieni'), ('Kohtalainen', 'Kohtalainen'), ('Suuri', 'Suuri')]
    )
    lannoituksentarve = SelectField(
        "Lannoituksentarve",
        choices=[('Pieni', 'Pieni'), ('Kohtalainen', 'Kohtalainen'), ('Suuri', 'Suuri')]
    )
    valontarve = SelectField(
        "Valontarve",
        choices=[('Pieni', 'Pieni'), ('Kohtalainen', 'Kohtalainen'), ('Suuri', 'Suuri')]
    )
    #kategoriat = QuerySelectMultipleField("Kategoriat", query_factory=Category.category_query, get_label="nimi")
    class Meta:
        csrf = False

class SearchForm(FlaskForm):
    nimi = StringField("Kasvin nimi")
    class Meta:
        csrf = False

class CategoryForm(FlaskForm):
    nimi = StringField("Kategorian nimi", [validators.Length(min=2, message="Nimen tulee olla vähintään 2 merkkiä pitkä")])
    kuvaus = StringField("Kategorian kuvaus", [validators.Length(min=2, message="Kuvauksen tulee olla vähintään 2 merkkiä pitkä")])
    class Meta:
        csrf = False

class SearchCategoryForm(FlaskForm):
    kategoria = QuerySelectField("Kategoria", query_factory=Category.category_query, get_label="nimi")
    class Meta:
        csrf = False
