from flask import session
from . import admin
from flask import request, render_template, abort, flash
from mod_users.forms import LoginForm
from mod_users.models import User


@admin.route('/')
def index():
    return 'Hello from admin Index'


@admin.route('/login', methods=['GET', 'POST'])
def login():
    # session['name'] = 'Roya'
    # session.clear()
    # print(session.get('name'))
    # print(session)
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            abort(400)
        # user = User.query.filter(User.email == form.email.data).first()
        user = User.query.filter(User.email.ilike('{}'.format(form.email.data))).first()
        if not user:
            flash('Invalid Credentials!', category='error')
            return render_template('admin/login.html', form=form)
        if not user.check_password(form.password.data):
            flash('Invalid Credentials!', category='warning')
            return render_template('admin/login.html', form=form)
        session['email'] = user.email
        session['user_id'] = user.id
        print(session)
        return 'Logged in Successfully!'
    if session.get('email') is not None:
        print(session)
        return 'You have been already logged!'
    return render_template('admin/login.html', form=form)
