import cpickle as pickle

file_name = 'recent_comments.p'

def overwrite_list(new_list, file_name):
    """
    Overwrite the currently stored list with a new one.
    """
    with open(file_name, 'wb+') as f:
        pickle.dump(new_list, f)

def get_list(file_name):
    """
    Unpickle and return the stored list.
    """
    with open(file_name, 'rb+') as f:
        current_list = pickle.load(f)
    return current_list

def update_list(new_item, file_name):
    """
    Update the stored list.
    Return the length of the updated list.
    The length is useful for triggering events.
    """
    current_list = get_list(file_name)
    current_list.append(new_item)
    overwrite_list(current_list, file_name)

    return len(current_list) + 1
