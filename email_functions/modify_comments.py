from email_functions.email_settings import *
from email_functions.format_email import *
from email_functions.send_email import *
from email_functions.modify_list import *

def add_to_recent_comments(comment):
    """
    add a comment to the recent_comments list.
    Return the length.
    """
    return update_list(comment, 'recent_comments.p')

def check_recent_comments_length(comments_length):
    """
    Check if the max comments length has been reached.
    Return a boolean value.
    """

    if length == max_comments:
        return True
    else:
        return False
