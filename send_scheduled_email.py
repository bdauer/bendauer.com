from email_functions.email_comments_interface import send_scheduled_email
from email_functions.email_settings import comments_file

"""
File for use with cron job.
"""

if __name__ == "__main__":
    send_scheduled_email(comments_file)
