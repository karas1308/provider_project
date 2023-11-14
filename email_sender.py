import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from constants import email_receiver, email_sender, subject, email_password


def mail_sender(_email_receiver, html=None):
    email_message = MIMEMultipart()
    email_message["From"] = email_sender
    email_message["To"] = _email_receiver
    # email_message["To"] = email_sender
    email_message["Subject"] = subject
    email_message.attach(MIMEText(html, "html"))
    _email_receiver = email_receiver
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        # smtp.sendmail(email_sender, "ihor.shchuka@gmail.com", email_message.as_string())
        # smtp.sendmail(email_sender, _email_receiver, email_message.as_string())
