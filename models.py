"""
models imports app, but app does not import models so we haven't created
any loops.
"""

import datetime
import re

from flask import Markup
from peewee import *
from markdown import markdown
from micawber import bootstrap_basic, parse_html
from markdown.extensions.extra import ExtraExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from playhouse.sqlite_ext import * #full text search
# from playhouse.flask_utils import FlaskDB

from settings import SITE_WIDTH

from app import app, db, database, oembed_providers


class BaseModel(db.Model):

    class Meta:

        database = database



# put this all in the models file. Eventually models folder for website.
class Entry(BaseModel):
    title = CharField()
    slug = CharField(unique=True)
    content = TextField()
    published = BooleanField(index=True)
    timestamp = DateTimeField(default=datetime.datetime.now, index=True)

    @property
    def html_content(self):
        """
        Generate HTML version of markdown-formatted blog entry
        and convert media URLS into embedded players/images.
        """
        hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()
        markdown_content = markdown(self.content, extensions=[hilite, extras])
        oembed_content = parse_html(
            markdown_content,
            oembed_providers,
            urlize_all=True,
            maxwidth=app.config['SITE_WIDTH'])
        return Markup(oembed_content)


    def save(self, *args, **kwargs):
        """
        Generate URL version of entry title.
        """
        if not self.slug:
            self.slug = re.sub('[^\w]+', '-', self.title.lower()).strip('-')
        ret = super(Entry, self).save(*args, **kwargs)

        # Store search content.
        self.update_search_index()
        return ret

    def update_search_index(self):
        """
        Create row in FTSEntry table with post content
        for full-text search using playhouse.sqlite_ext.
        """
        query = (FTSEntry
                 .select(FTSEntry.docid, FTSEntry.entry_id)
                 .where(FTSEntry.entry_id == self.id))
        try:
            fts_entry = query.get()
        except FTSEntry.DoesNotExist:
            fts_entry = FTSEntry(entry_id=self.id)
            force_insert = True
        else:
            force_insert = False
        fts_entry.content = '\n'.join((self.title, self.content))
        fts_entry.save(force_insert=force_insert)

    @classmethod
    def public(cls):
        return Entry.select().where(Entry.published == True)

    @classmethod
    def drafts(cls):
        return Entry.select().where(Entry.published == False)

    @classmethod
    def search(cls, query):
        words = [word.strip() for word in query.split() if word.strip()]
        if not words:
            # Return empty query.
            return Entry.select().where(Entry.id == 0)
        else:
            search = ' '.join(words)

        # Query full-text search index for matching entries
        # then join entry data on the matching result.
        return (FTSEntry
                .select(
                    FTSEntry,
                    Entry,
                    FTSEntry.rank().alias('score'))
                .join(Entry, on=(FTSEntry.entry_id == Entry.id).alias('entry'))
                .where(
                    (Entry.published == True) &
                    (FTSEntry.match(search)))
                .order_by(SQL('score').desc()))


class Comment(BaseModel):
    # build out the comment here. Maybe use oauth2 for comments and log users.
    name = CharField()
    content = TextField()
    email = CharField()
    website = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now, index = True)

    entry = ForeignKeyField(Entry, related_name = 'comments')

    class Meta:
        order_by =('-timestamp',)

    @property
    def html_content(self):
        """
        Generate HTML version of markdown-formatted blog entry
        and convert media URLS into embedded players/images.
        """
        hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()
        markdown_content = markdown(self.content, extensions=[hilite, extras])
        oembed_content = parse_html(
            markdown_content,
            oembed_providers,
            urlize_all=True,
            maxwidth=app.config['SITE_WIDTH'])
        return Markup(oembed_content)

class FTSEntry(FTSModel):
    entry_id = IntegerField()
    content = TextField()

    class Meta:
        database = database
