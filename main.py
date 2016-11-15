from app import app, db
from models import *
from views import *

def main():
    db.create_tables([Entry, FTSEntry, Comment], safe=True)
    app.run(debug=False)

if __name__ == '__main__':
    main()
