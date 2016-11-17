from modify_comments import (add_to_recent_comments, get_recent_comments,
                             check_recent_comments_length, reset_comments_list)

from email_settings import (from_email, from_password, smtp_host, port,
                            comments_file, to_email_for_comments, max_comments)

from send_email import send_email_via_smtp
from format_email import format_email, format_subject


def run_email_update(comment):
    """
    Checks if the new comments queue has reached its threshold.
    If it has, sends an email.
    """
    recent_comments = add_to_recent_comments(comment, comments_file)

    if _comments_threshold_met(max_comments, recent_comments):
        _send_email_and_reset_recent_comments_list(recent_comments)


def send_scheduled_email(comments_file):
    """
    Checks if there are any new comments.
    If there are, sends an email.

    Used for cronjob.
    """
    print("It began running.")
    recent_comments = get_recent_comments(comments_file)
    print("It accessed recent_comments")
    print (recent_comments)

    if _comments_threshold_met(1, recent_comments):
        print("The threshold was met")
        _send_email_and_reset_recent_comments_list(recent_comments)
        print("Send email ran")


def _comments_threshold_met(threshold, recent_comments):
    """
    Returns true if the comments threshold is met,
    otherwise returns false.
    """
    if len(recent_comments) >= threshold:
        return True
    else:
        return False


def _send_email_and_reset_recent_comments_list(recent_comments):
    """
    Sends an email and resets the recent_comments list.
    """
    formatted_subject, formatted_email = \
    _build_new_comments_email(recent_comments)

    send_email_via_smtp(from_email, from_password, to_email_for_comments,\
                        formatted_subject, formatted_email, smtp_host, port)

    reset_comments_list(comments_file)


def _build_new_comments_email(comments):
    """
    Return the fields that need to be generated for sending a comments email.
    """
    subject = "New comments at bendauer.com"
    formatted_subject, formatted_email = format_email(comments, subject)

    return (formatted_subject, formatted_email)
