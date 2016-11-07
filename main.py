from app import app, db
from models import *
from views import *

def main():
    database.create_tables([Entry, FTSEntry, Comment], safe=True) # add comments with entry id.
    app.run(debug=True)

if __name__ == '__main__':
    main()
