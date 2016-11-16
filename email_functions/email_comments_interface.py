from modify_comments import *
from email_settings import *
from send_email import *


def run_email_update(comment):
    """
    Checks if conditions for sending comments email have been met.
    If they have, sends an email.
    """
    updated_comments_length = add_to_recent_comments(comment)
    is_maxed = check_recent_comments_length(updated_comments_length)

    if is_maxed:
        # create and send an email.
        comments = get_recent_comments(file_name)
        formatted_email = format_email(comments)
        formatted_subject = format_subject("New comments at bendauer.com")
        send_email_via_smtp(from_email, from_password, to_email_for_comments,\
                            formatted_subject, formatted_email, smtp_host, port)
        overwrite_list(list(), file_name)
