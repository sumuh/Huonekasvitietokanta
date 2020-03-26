from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators

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

    class Meta:
        csrf = False
