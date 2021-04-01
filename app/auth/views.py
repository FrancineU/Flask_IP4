from flask import render_template, redirect, url_for, flash, request
from . import auth
from flask_login import login_user, logout_user, login_required
from ..models import Writer
from .forms import SignupForm, LoginForm
from .. import db

@auth.route('/signup', methods = ["POST", "GET"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        writer = Writer(fullname = form.fullname.data, email = form.email.data, password = form.password.data)
        writer.save_writer()

        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', signup_form = form)

@auth.route('/login', methods = ["POST", "GET"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        writer = Writer.query.filter_by(email = form.email.data).first()
        if writer is not None and writer.verify_password(form.password.data):
            login_user(writer, form.remember.data)
            return redirect(request.args.get('next') or url_for('main.writer_profile', uname = writer.email))

        flash('Invalid username or Password')

    return render_template('auth/login.html', login_form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))