from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class CarForm(FlaskForm):
    name = StringField('Car Name', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    mileage = IntegerField('Mileage (km)', validators=[DataRequired()])
    submit = SubmitField('Submit')
