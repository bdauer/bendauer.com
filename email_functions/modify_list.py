import cPickle as pickle


def overwrite_list(new_list, file_name):
    """
    Overwrite the currently stored list with a new one.
    """
    with open(file_name, 'w') as f:
        pickle.dump(new_list, f)

def get_list(file_name):
    """
    Unpickle and return the stored list.
    """
    try:
        with open(file_name, 'r+') as f:
            current_list = pickle.load(f)
    except IOError:
        print("There was an IOError")
        with open(file_name, 'w') as f:
            current_list = []
    except EOFError:
        print("There was an EOFError")
        current_list = []

    return current_list

def update_list(new_item, file_name):
    """
    Update the stored list.
    Return the current_list.
    """
    current_list = get_list(file_name)
    current_list.append(new_item)
    overwrite_list(current_list, file_name)

    return current_list
