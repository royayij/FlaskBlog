from . import blog
from flask import render_template
from mod_blog.models import Post, Category


@blog.route('/')
def index():
    posts = Post.query.all()
    return render_template('blog/index.html', posts=posts)


@blog.route('/<string:slug>')
def single_post(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('blog/single_post.html', post=post)


@blog.route('/category/<string:slug>')
def single_category(slug):
    category = Category.query.filter(Category.slug == slug).first_or_404()
    return render_template('blog/single_category.html', category=category)