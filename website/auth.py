from dataclasses import dataclass
import re
from flask import Blueprint, flash, render_template, url_for, redirect, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():

    if request.method=='POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("logged in", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Please enter correct details", category="error")
        else:
            flash("User doesnt exist!")

    return render_template("login.html", user= current_user)

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method== 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        role = request.form.get("role")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        print(role)
        
        email_exits = User.query.filter_by(email = email).first()
        if email_exits:
            flash("User already exists in the system", category="error")
        elif password1 != password2:
            flash("Password doesnt match", category="error")
        elif len(password1) < 6: 
            flash("Password is too short", category="error")
        else: 
            new_user = User(username=username, email=email,role= role, password= generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created')

            return redirect(url_for("views.home"))

    return render_template("signup.html", user= current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


@auth.route("/managerapproval")
@login_required
def managerapproval():
    return redirect(url_for("views.home"))


@auth.route("/aboutus", methods=['GET'])
def aboutus():
    return render_template("aboutus.html", user= current_user)



@auth.route("/contactus", methods=['GET'])
def contactus():
    return render_template("contactus.html", user= current_user)
