from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, URL, Email

YES_NO = ['❌', '✔️']

class CafeForm(FlaskForm):
    name = StringField('Cafe Name', [DataRequired()])
    map_url = StringField('Location Link', [DataRequired(), URL()])
    img_url = StringField('Image Link', [DataRequired(), URL()])
    location = StringField('Location', [DataRequired()])
    has_sockets = SelectField('Has Sockets', choices=YES_NO)
    has_toilet = SelectField('Has Toilets', choices=YES_NO)
    has_wifi = SelectField('Has Wifi', choices=YES_NO)
    can_take_calls = SelectField('Can Take Calls', choices=YES_NO)
    seats = StringField('Seating Capacity', [DataRequired()])
    coffee_price = StringField('Coffee Price', [DataRequired()])
    submit = SubmitField(label="Submit")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")