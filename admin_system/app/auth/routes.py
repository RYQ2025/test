from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse # Changed from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User # Needed to query the User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index')) # Assuming a main.index route
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '': # Changed url_parse to urlparse
            next_page = url_for('main.index') # Default redirect to main index
        flash('Logged in successfully!', 'success')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
@login_required # User must be logged in to log out
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index')) # Redirect to main index (or login page)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, your registration is complete! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)
