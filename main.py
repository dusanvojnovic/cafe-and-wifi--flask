from flask import Flask, render_template, url_for, redirect, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CafeForm, RegisterForm, LoginForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Bootstrap(app)
app.secret_key = "myveryverysecretkey"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

db.create_all()

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    has_sockets = db.Column(db.Integer, nullable=False)
    has_toilet = db.Column(db.Integer, nullable=False)
    has_wifi = db.Column(db.Integer, nullable=False)
    can_take_calls = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.String(100), nullable=False)
    coffee_price = db.Column(db.String(100), nullable=False)
# db.create_all() # Don't really need this statement since it's to create the database, which was already downloaded for the assignment

def yes_no(option):
    if option == '✔️':
        return 1
    else:
        return 0

def check_does_have(option):
    if option == 1:
        return '✔️'
    else:
        return '❌'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/cafes')
def cafes():
    return render_template("cafes.html", cafes=db.session.query(Cafe).all())

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            flash("You've already signed up with that email, log in instead.")
            return redirect(url_for("login"))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method = "pbkdf2:sha256",
            salt_length = 5
        )
    
        new_user = User(
            email = form.email.data,
            password = hash_and_salted_password
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("cafes"))

    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # email doesn't exist
        if not user:
            flash("That email does not exist, please try again")
            return redirect(url_for('login'))
        # password incorrect
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for("cafes"))
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/add', methods = ["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name = form.name.data,
            map_url = form.map_url.data,
            image_url = form.img_url.data,
            location = form.location.data,
            has_sockets = yes_no(form.has_sockets.data),
            has_toilet = yes_no(form.has_toilet.data),
            has_wifi = yes_no(form.has_wifi.data),
            can_take_calls = yes_no(form.can_take_calls.data),
            seats = form.seats.data,
            coffee_price = form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()

        return redirect(url_for("cafes"))
    return render_template("add.html", form = form)

@app.route('/edit/<id>', methods = ["GET", "POST"])
def edit(id):
    cafe_to_edit = Cafe.query.get(id)
    form = CafeForm(
        name = cafe_to_edit.name,
        map_url = cafe_to_edit.map_url,
        img_url = cafe_to_edit.img_url,
        location = cafe_to_edit.location,
        has_sockets = check_does_have(cafe_to_edit.has_sockets),
        has_toilet = check_does_have(cafe_to_edit.has_toilet),
        has_wifi = check_does_have(cafe_to_edit.has_wifi),
        can_take_calls = check_does_have(cafe_to_edit.can_take_calls),
        seats = cafe_to_edit.seats,
        coffee_price = cafe_to_edit.coffee_price
    )

    if form.validate_on_submit():
        cafe_to_edit = Cafe.query.get(id)
        
        cafe_to_edit.name = form.name.data
        cafe_to_edit.map_url = form.map_url.data
        cafe_to_edit.img_url = form.img_url.data
        cafe_to_edit.locaiton = form.location.data
        cafe_to_edit.has_sockets = yes_no(form.has_sockets.data)
        cafe_to_edit.has_toilet = yes_no(form.has_toilet.data)
        cafe_to_edit.has_wifi = yes_no(form.has_wifi.data)
        cafe_to_edit.can_take_calls = yes_no(form.can_take_calls.data)
        cafe_to_edit.seats = form.seats.data
        cafe_to_edit.coffe_price = form.coffee_price.data

        db.session.commit()

        return redirect(url_for("cafes"))
    
    return render_template("add.html", form = form)

@app.route("/delete/<id>", methods = ["GET", "POST"])
def delete(id):
    cafe_to_delete = Cafe.query.get(id)
    db.session.delete(cafe_to_delete)
    db.session.commit()

    return redirect(url_for("home"))



if __name__ == '__main__':
    app.run(debug=True)