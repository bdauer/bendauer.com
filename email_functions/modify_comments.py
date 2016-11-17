from email_settings import *
from format_email import *
from send_email import *
from modify_list import *


def add_to_recent_comments(comment):
    """
    add a comment to the recent_comments list.
    Return the  recent_comments list.
    """
    return update_list(comment, 'recent_comments.p')


def check_recent_comments_length(comments_length):
    """
    Check if the max comments length has been reached.
    Return a boolean value.
    """
    if comments_length >= max_comments:
        return True
    else:
        return False


def get_recent_comments(file_name):
    """
    Return the recent_comments list.
    """
    return get_list(file_name)


def reset_comments_list(file_name):
    overwrite_list(list(), file_name)
