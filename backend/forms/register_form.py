from wtforms import StringField, PasswordField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    #Remove username since it's generated
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])

    #Patient-related fields
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=50)])
    age = IntegerField('Age', validators=[InputRequired(), NumberRange(min=1, max=120)])
    gender = IntegerField('Gender', validators=[InputRequired(), NumberRange(min=0, max=1)])  #0 for male, 1 for female
    ethnicity = IntegerField('Ethnicity', validators=[InputRequired()])
    diagnosis = IntegerField('Diagnosis', validators=[InputRequired()])  #0 for non-diabetic, 1 for diabetic
    smoking = BooleanField('Smoking', validators=[InputRequired()])  #True for smoker, False for non-smoker
    family_history_diabetes = BooleanField('Family History of Diabetes', default=False)
