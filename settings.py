import os
import hashlib

h = hashlib.sha1()
h.update('add password here')
ADMIN_PASSWORD = h.digest()

APP_DIR = os.path.dirname(os.path.realpath(__file__))

DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'blog.db')
DEBUG = False

SECRET_KEY = 'secret key goes here'

# used by micawber to generate rich media embedded objects at this maxwidth
SITE_WIDTH = 800
