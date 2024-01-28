from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from backend.app.models import User, RegistrationForm, Profile
from backend.config import Config

app = Flask(__name__, template_folder='frontend/templates')
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


login_manager = LoginManager(app)
login_manager.login_view = 'Login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
