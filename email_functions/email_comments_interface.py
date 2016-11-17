from modify_comments import (add_to_recent_comments, get_recent_comments,
                             check_recent_comments_length, reset_comments_list)

from email_settings import (from_email, from_password, smtp_host, port,
                            comments_file, to_email_for_comments)

from send_email import send_email_via_smtp


def run_email_update(comment):
    """
    Checks if conditions for sending comments email have been met.
    If they have, sends an email.
    """
    updated_comments_length = add_to_recent_comments(comment)
    is_maxed = check_recent_comments_length(updated_comments_length)

    if is_maxed:
        # create and send an email.
        comments, formatted_subject, formatted_email = \
        _build_new_comments_email()
        # comments = get_recent_comments(comments_file)
        # formatted_email = format_email(comments)
        # formatted_subject = format_subject("New comments at bendauer.com")
        send_email_via_smtp(from_email, from_password, to_email_for_comments,\
                            formatted_subject, formatted_email, smtp_host, port)
        reset_comments_list(comments_file)


def send_scheduled_email(comments_file):
    """
    Used for cronjob. Sends an email containing the comments.
    """
    recent_comments = get_recent_comments(comments_file)

    if len(recent_comments) >= 1:
        comments, formatted_subject, formatted_email = \
        _build_new_comments_email()

        send_email_via_smtp(from_email, from_password, to_email_for_comments,\
                            formatted_subject, formatted_email, smtp_host, port)

        reset_comments_list(comments_file)

def _build_new_comments_email():
    """
    Return the fields that need to be generated for sending a comments email.
    """
    comments = get_recent_comments(comments_file)
    formatted_email = format_email(comments)
    formatted_subject = format_subject("New comments at bendauer.com")

    return (comments, formatted_subject, formatted_email)

if __name__ == "__main__":
    send_scheduled_email(comments_file)
