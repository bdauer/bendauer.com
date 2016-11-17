import datetime

def format_email(comments, subject):
    """
    Return the formatted subject line, and
    a formatted email
    containing a series of formatted comments
    and the range of time during which they were added.

    Keyword arguments:
    Comments -- a list of comment objects
    representing comment entries in the database.
    """

    formatted_subject = format_subject(subject)
    start_range, end_range = get_timeframe(comments)

    start = "The following comments arrived between {0} and {1}.\n\n"\
            .format(start_range, end_range)

    middle = ""

    for comment in comments:
        middle += format_comment(comment.name, comment.content,\
                                 comment.timestamp, comment.entry.title)

    end = "_____"

    return (formatted_subject, start + middle + end)


def format_subject(subject):
    """
    Returns a subject line formatted for smtp, for the comments email.
    """
    return "Subject: {0}".format(subject)

def format_comment(name, content, timestamp, entry):
    """
    Return a comment formatted for emailing.


    Keyword arguments:
    name, content, timestamp -- from the comment object
    entry --  the title of the entry
    """
    datetime = timestamp.strftime('%m/%d/%Y at %I:%M%p')
    start = "{0} added a comment to '{1}' on {2}\n".format(\
                                    name, entry, datetime)
    middle = "They said: '{0}'".format(content)
    end = "\n\n"
    return start + middle + end


def get_timeframe(comments):
    """
    Return a tuple containing the earliest and latest timestamps
    of the comments in the list in a readable format.
    """
    comment_times = [comment.timestamp for comment in comments]
    # for comment in comments:
    #     comment_times.append(comment.timestamp)
    return (min(comment_times).strftime('%m/%d/%Y at %I:%M%p'),\
           max(comment_times).strftime('%m/%d/%Y at %I:%M%p'))
