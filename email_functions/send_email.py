import smtplib
from email_settings import from_email, from_password, port

def send_email_via_smtp(from_email, from_password, to_email,
                        subject, body, smtp_host, port):
    """
    Sends an email over smtp.
    """
    contents = subject + "\n" + body

    smtp_object = create_smtp_object(from_email, from_password, smtp_host, port)

    smtp_object.login(from_email, from_password)
    send_email(smtp_object, from_email, to_email, contents)
    smtp_object.quit()



def create_smtp_object(from_email, from_password, smtp_host, port):
    """
    Connects to a provided SMTP host using TLS or SSL encryption,
    depending on the port.
    Returns an smtp_object representing the connection.
    """
    if port == 587:
        using_TLS = True

    if using_TLS:
        smtp_object = smtplib.SMTP(smtp_host, port)
    else:
        smtp_object = smtplib.SMTP_SSL(smtp_host, port)

    smtp_object.ehlo()

    if using_TLS:
        smtp_object.starttls()

    return smtp_object

def send_email(smtp_object, from_email, to_email, contents):
    """
    Sends an email over an smtp connection.
    If there are multiple recipients, to_email should be a list.
    """
    smtp_object.sendmail(from_email, to_email, contents)
    smtp_object.quit()

if __name__ == '__main__':
    send_email_via_smtp(from_email, from_password, to_email,
                            subject, body, smtp_host, port)
