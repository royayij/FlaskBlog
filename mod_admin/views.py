from . import admin
from flask import request, render_template, abort, flash, session, redirect, url_for
from mod_users.forms import LoginForm, RegisterForm
from mod_users.models import User
from .utils import admin_only_view
from mod_blog.forms import CreatePostForm, ModifyPostForm, CreateCategoryForm, ModifyCategoryForm
from mod_blog.models import Post, Category
from app import db
from sqlalchemy.exc import IntegrityError


@admin.route('/')
@admin_only_view
def index():
    return render_template('admin/index.html')


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
        if not user.is_admin():
            flash('Invalid Credentials!', category='error')
            return render_template('admin/login.html', form=form)
        session['email'] = user.email
        session['user_id'] = user.id
        session['role'] = user.role
        print(session)
        return redirect(url_for('admin.index'))
    if session.get('role') == 1:
        print(session)
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html', form=form)


@admin.route('/logout', methods=['GET'])
@admin_only_view
def logout():
    session.clear()
    flash('You logged out successfully', category='warning')
    return redirect(url_for('admin.login'))


@admin.route('create/new', methods=['GET', 'POST'])
def create_post():
    form = CreatePostForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            abort(400)
        post = Post()
        post.title = form.title.data
        post.slug = form.slug.data
        post.summary = form.summary.data
        post.content = form.content.data
        try:
            db.session.add(post)
            db.session.commit()
            flash("Post Created!")
            return redirect(url_for('admin.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Post is ')
            return render_template('admin/create_post.html', form=form)
    return render_template('admin/create_post.html', form=form)


@admin.route('/users', methods=['GET'])
@admin_only_view
def list_users():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('admin/list_users.html', users=users)


@admin.route('/users/new', methods=['GET'])
@admin_only_view
def create_user():
    form = RegisterForm()
    return render_template('admin/create_user.html', form=form)


@admin.route('/users/new', methods=['POST'])
@admin_only_view
def create_user_post():
    form = RegisterForm(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('admin.create_user'))
    if not form.password.data == form.confirm_password.data:
        error_msg = 'Password and Confirm Password does not match!'
        form.password.errors.append(error_msg)
        form.confirm_password.errors.append(error_msg)
        return render_template('admin/create_user.html', form=form)
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
    return render_template('admin/create_user.html', form=form)


@admin.route('/posts')
@admin_only_view
def list_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('admin/list_posts.html', posts=posts)


@admin.route('/posts/delete/<int:post_id>')
@admin_only_view
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted.')
    return redirect(url_for('admin.list_posts'))


@admin.route('/posts/modify/<int:post_id>', methods=['GET', 'POST'])
@admin_only_view
def modify_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = ModifyPostForm(obj=post)
    if request.method == 'POST':
        if not form.validate_on_submit():
            abort(400)
        post.title = form.title.data
        post.slug = form.slug.data
        post.summary = form.summary.data
        post.content = form.content.data
        try:
            db.session.commit()
            flash("Post Modified!")
            return redirect(url_for('admin.list_posts'))
        except IntegrityError:
            db.session.rollback()
            flash('slug duplicated')
            return redirect(url_for('admin.list_posts'))
    return render_template('admin/modify_post.html', form=form, post=post)


@admin.route('/categories/new', methods=['GET', 'POST'])
@admin_only_view
def create_category():
    form = CreateCategoryForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            abort(400)
        category = Category()
        category.name = form.name.data
        category.slug = form.slug.data
        category.description = form.description.data
        try:
            db.session.add(category)
            db.session.commit()
            flash('Category created!')
            return redirect(url_for('admin.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Slug Duplicated.')
            return render_template('admin/create_category.html', form=form)
    return render_template('admin/create_category.html', form=form)


@admin.route('/categories')
@admin_only_view
def list_categories():
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/list_categories.html', categories=categories)


@admin.route('/categories/delete/<int:category_id>')
@admin_only_view
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category Deleted.')
    return redirect(url_for('admin.list_categories'))


@admin.route('/categories/modify/<int:category_id>', methods=['GET', 'POST'])
@admin_only_view
def modify_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = ModifyCategoryForm(obj=category)
    if request.method == 'POST':
        if not form.validate_on_submit():
            abort(400)
        category.name = form.name.data
        category.slug = form.slug.data
        category.description = form.description.data
        try:
            db.session.commit()
            flash("Category Modified!")
            return redirect(url_for('admin.list_categories'))
        except IntegrityError:
            db.session.rollback()
            flash('slug duplicated')
            return redirect(url_for('admin.list_categories'))
    return render_template('admin/modify_category.html', form=form, category=category)