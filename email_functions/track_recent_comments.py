import cpickle as pickle

def add_to_list(recent_comments, count):
    with open('recent_comments.p', 'wb+') as f:
        pickle.dump(count, f)
        pickle.dump(recent_comments, f)

def get_count_and_list():
    with open('recent_comments.p', 'rb') as f:
        count = pickle.load(f)
        recent_comments = pickle.load(f)
    return (count, recent_comments)

def get_count():
    with open('recent_comments.p', 'rb') as f:
        count = pickle.load(f)
    return count
