from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, validators, RadioField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from application.auth.models import User
from .models import Plant, PlantUser, Category, PlantCategory

class PlantForm(FlaskForm):

    name_fin = StringField("Kasvin nimi", [validators.Length(min = 2, message = "Nimen tulee olla vähintään 2 merkkiä pitkä")])
    name_lat = StringField("Latinankielinen nimi", [validators.Length(min = 2, message = "Nimen tulee olla vähintään 2 merkkiä pitkä")])
    water_need = SelectField(
        "Vedentarve",
        choices = [('Pieni', 'Pieni'), ('Kohtalainen', 'Kohtalainen'), ('Suuri', 'Suuri')]
    )
    fertilizer_need = SelectField(
        "Lannoituksentarve",
        choices = [('Pieni', 'Pieni'), ('Kohtalainen', 'Kohtalainen'), ('Suuri', 'Suuri')]
    )
    light_need = SelectField(
        "Valontarve",
        choices = [('Pieni', 'Pieni'), ('Kohtalainen', 'Kohtalainen'), ('Suuri', 'Suuri')]
    )
    class Meta:
        csrf = False

class SearchPlantForm(FlaskForm):

    name_fin = StringField("Kasvin nimi")
    class Meta:
        csrf = False

class CategoryForm(FlaskForm):

    name = StringField("Kategorian nimi", [validators.Length(min = 2, message = "Nimen tulee olla vähintään 2 merkkiä pitkä")])
    description = StringField("Kategorian kuvaus", [validators.Length(min = 2, message = "Kuvauksen tulee olla vähintään 2 merkkiä pitkä")])
    class Meta:
        csrf = False

class SearchCategoryForm(FlaskForm):

    category = QuerySelectField("Kategoria", query_factory = Category.category_query, get_label = "name")
    class Meta:
        csrf = False

class UpdateLastWateredForm(FlaskForm):

    newdate = DateField("Date", format = "%d/%m/%Y")
    class Meta:
        csrf = False

class UpdateLastFertilizedForm(FlaskForm):

    newdate = DateField("Date", format = "%d/%m/%Y")
    class Meta:
        csrf = False
