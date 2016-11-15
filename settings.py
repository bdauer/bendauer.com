import os
import hashlib

h = hashlib.sha1()
h.update('thisismypassword')
ADMIN_PASSWORD = h.digest()

APP_DIR = os.path.dirname(os.path.realpath(__file__))

DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'blog.db')
DEBUG = False

SECRET_KEY = 'v\x99!\x12\xce{\xa3\xb0\x96\x86\xe3\xc4\xf7g\r\x04Q\x08\xa9\xbf\x02)\x0fy'

# used by micawber to generate rich media embedded objects at this maxwidth
SITE_WIDTH = 800
