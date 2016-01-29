from .. import app, db_session, \
               Item, Category, BaseForm, \
               flash_errors, slugify_category_list
from flask.ext.login import current_user, login_user, login_required
from flask import flash, redirect, url_for, render_template, request
from wtforms import StringField, PasswordField, TextAreaField, HiddenField, \
                    SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class SearchForm(BaseForm):
    query = StringField('Search',
                        validators=[
                            DataRequired()])
    categories = SelectMultipleField('Categories')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    form.categories.choices = [(g.id, g.name) for g
                               in db_session.query(Category).order_by('name')]
    page = request.form.get('page', 1)
    filter_query = request.form.get('query', False)
    filter_filterbycat = 'filterbycat' in request.form
    filter_categories = request.form.getlist('categories[]')
    items = db_session.query(Item).all()[(page-1)*10::10]
    if filter_query is not False:
        items = db_session.query(Item) \
            .filter((Item.name.ilike(filter_query)) |
                    (Item.description.ilike(filter_query))) \
            .all()[(page-1)*10::10]
    return render_template('index.html', form=form, items=items)