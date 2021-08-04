from . import users
from sqlalchemy.exc import IntegrityError
from app import db
from flask import request, abort, flash, render_template
from .forms import RegisterForm
from .models import User


@users.route('/')
def index():
    return "Hello from users page."


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('users/register.html', form=form)
        if not form.password.data == form.confirm_password.data:
            error_msg = 'Password and Confirm Password does not match!'
            form.password.errors.append(error_msg)
            form.confirm_password.errors.append(error_msg)
            return render_template('users/register.html', form=form)
        user = User()
        user.full_name = form.full_name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('You created your account')
        except IntegrityError:
            db.session.rollback()
            flash('Email in use!', category='error')
    return render_template('users/register.html', form=form)
