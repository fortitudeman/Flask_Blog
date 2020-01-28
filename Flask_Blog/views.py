"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, url_for, flash, request, redirect
from Flask_Blog import app
from Flask_Blog.forms import RegistrationForm, LoginForm
from Flask_Blog import db
from Flask_Blog.models import User, Post
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required


bcrypt = Bcrypt(app)

posts = [
     {
        'author':'Jack Dawson',
        'title':'Blog Post1',
        'content': 'About Titanic',
        'date_posted':'April 15, 1912'
     },
     {
        'author':'Rose Buchater',
        'title':'Blog Post2',
        'content': 'About Titanic',
        'date_posted':'April 15, 1912'
     },
    ]

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'home.html',
        posts = posts,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registered Successully! Now You can Log in','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Failed! Please Check username and password','danger')
    return render_template('login.html', title='title', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('contact'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='account')