import functools
import urllib
import hashlib

from flask import (Flask, abort, flash, redirect, render_template, request,
                   session, url_for, Response)
from playhouse.flask_utils import get_object_or_404, object_list
from peewee import *

from app import app, database, db
from models import Entry, Comment, FTSEntry
from settings import ADMIN_PASSWORD
from email_functions.email_comments_interface import run_email_update

def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return inner

@app.route('/login/', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('password'):
        h = hashlib.sha1()
        h.update(request.form.get('password'))
        password = h.digest()
        # password = request.form.get('password')
        # TODO after adding a one-way hash, hash the user-submitted
        # password and compare to the hashed version.
        if password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session.permanent = True # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('blog'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('login.html', next_url=next_url)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    return render_template('logout.html')


@app.route('/')
def index():
    query = Entry.public().select().order_by(Entry.timestamp.desc()).limit(1)
    entry = query.get()

    return render_template('index.html', entry=entry)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog/')
def blog():
    # The `object_list` helper will take a base query and then handle
    # paginating the results if there are more than 20. For more info see
    # the docs:
    # http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#object_list

    search_query = request.args.get('q')

    if search_query:
        query = Entry.search(search_query)
    else:
        query = Entry.public().order_by(Entry.timestamp.desc())
    return object_list('blog.html',
                       query,
                       search=search_query,
                       check_bounds=False,
                       paginate_by=10)

def _create_or_edit(entry, template):
    if request.method == 'POST':
        entry.title = request.form.get('title') or ''
        entry.content = request.form.get('content') or ''
        entry.published = request.form.get('published') or False
        if not (entry.title and entry.content):
            flash('title and content are required.', 'danger')
        else:
            # Wrap the call to save in a transaction so we can roll it back
            # cleanly in the event of an integrity error.
            try:
                with database.atomic():
                    entry.save()
            except IntegrityError:
                flash('Error: this title is already in use.', 'danger')
            else:
                flash('Entry saved successfully.', 'success')
                if entry.published:
                    return redirect(url_for('detail', slug=entry.slug))
                else:
                    return redirect(url_for('edit', slug=entry.slug))

    return render_template(template, entry=entry)

@app.route('/blog/create/', methods=['GET', 'POST'])
@login_required
def create():
    return _create_or_edit(Entry(title='', content=''), 'create.html')


@app.route('/drafts/')
@login_required
def drafts():
    query = Entry.drafts().order_by(Entry.timestamp.desc())
    return object_list('blog.html', query)

# create/drafts comes first so that it's not read as a slug
@app.route('/blog/<slug>/', methods=['GET', 'POST'])
def detail(slug):
    if session.get('logged_in'):
        query = Entry.select()
    else:
        query = Entry.public()
    entry = get_object_or_404(query, Entry.slug == slug)
    comments = entry.comments
    comment = Comment(name='', content='', entry=entry)

    if request.method == 'GET':
        return render_template('detail.html', entry=entry, comments=comments)

    if request.method == 'POST':
        comment.name = request.form.get('name') or ''
        comment.website = request.form.get('website') or ''
        comment.email = request.form.get('email') or ''
        comment.content = request.form.get('content') or ''

        # if not (comment.name and comment.email and comment.content):
            # flash('name, email and comment are required.', 'danger')
        # else:
        with database.atomic():
            comment.save()
            run_email_update(comment)


            # flash('comment saved successfully.', 'success')
        return redirect(url_for('detail', slug=entry.slug))
        # return render_template('detail.html', entry=entry, comments=comments)

@login_required
@app.route('/blog/<slug>/<comment_id>/del')
def delete_comment(slug, comment_id):
    comment = Comment.get(Comment.id == comment_id)
    comment.delete_instance()
    return redirect(url_for('detail', slug=slug)+'#comments')

@app.route('/blog/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
    entry = get_object_or_404(Entry, Entry.slug == slug)
    return _create_or_edit(entry, 'edit.html')

@app.template_filter('clean_querystring')
def clean_querystring(request_args, *keys_to_remove, **new_values):
    querystring = dict((key, value) for key, value in request_args.items())
    for key in keys_to_remove:
        querystring.pop(key, None)
    querystring.update(new_values)
    return urllib.urlencode(querystring)

@app.errorhandler(404)
def not_found(exc):
    return Response("<h3>Someday I'll have a better 404 error.</h3>"), 404
