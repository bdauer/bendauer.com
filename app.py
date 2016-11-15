



from flask import (Flask, abort, flash, Markup, redirect, render_template,
                   request, Response, session, url_for)
from markdown import markdown
from micawber import bootstrap_basic, parse_html
from micawber.cache import Cache as OEmbedCache
from peewee import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
from playhouse.sqlite_ext import * #full text search


#this stays in app.py
app = Flask(__name__)
app.config.from_pyfile('settings.py')

# FlaskDB wrapper for peewee db that setus up pre/post-request hooks for
# db connections
db = FlaskDB(app)
database = db.database

# Used as list for micawber
oembed_providers = bootstrap_basic(OEmbedCache())

if __name__ == '__main__':
    app.run(debug=False)
