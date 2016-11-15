from app import app, database
from models import *
from views import *

def main():
    database.create_tables([Entry, FTSEntry, Comment], safe=True)
    app.run(debug=False)

if __name__ == '__main__':
    main()
