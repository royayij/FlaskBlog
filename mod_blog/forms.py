from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired
from utils.forms import MultipleCheckBox


class PostForm(FlaskForm):
    title = TextField(validators=[DataRequired()])
    summary = TextAreaField()
    content = TextAreaField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
    categories = MultipleCheckBox(coerce=int)


class CategoryForm(FlaskForm):
    description = TextAreaField()
    name = TextField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])


class SearchForm(FlaskForm):
    search_query = TextField(validators=[DataRequired()])
