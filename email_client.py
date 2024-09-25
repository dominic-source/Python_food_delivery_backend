"""
email_client.py

This module handles the sending of emails. It provides functionalities 
to send emails with retry logic and to construct email messages with 
HTML content.
"""

import smtplib
import os
from time import sleep
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tenacity import retry, stop_after_attempt, after_log
import logging

# Configure logging
logging.basicConfig(filename='consumer.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), after=after_log(logger, logging.DEBUG))
async def send_mail(sen, pas, addr, port, rec, message):
    """
    Send an email using the specified SMTP server.

    Args:
        sen (str): Sender's email address.
        pas (str): Sender's email password.
        addr (str): SMTP server address.
        port (int): SMTP server port.
        rec (str): Recipient's email address.
        message (str): The email message to send.

    Returns:
        None
    """
    server = smtplib.SMTP_SSL(addr, port)
    server.login(sen, pas)
    server.sendmail(sen, rec, message)
    server.quit()
    

async def mailSender(id=None, subj=None, mess=None, addr="smtp.gmail.com", pas=None, 
                     sen=None, rec=None, port=465):
    """
    Prepare and send an email.

    Args:
        id (str, optional): User ID (not used in this function but kept for compatibility).
        subj (str, optional): Subject of the email.
        mess (str, optional): Message content of the email.
        addr (str): SMTP server address. Default is "smtp.gmail.com".
        pas (str, optional): Sender's email password. If not provided, it is loaded from environment variables.
        sen (str, optional): Sender's email address.
        rec (str, optional): Recipient's email address.
        port (int): SMTP server port. Default is 465.

    Returns:
        None
    """
    if sen is None or rec is None:
        return
    
    # Load environmental variables
    load_dotenv()

    # Get the environmental variable which has the password or use argument password
    if pas is None:
        pas = os.getenv("GTP")

    # Prepare the email message
    message = MIMEMultipart()
    message['From'] = sen
    message['To'] = rec
    message['Subject'] = subj if subj else "Email communication"
    
    if mess is None:
        mess = "Software engineering is good, but also has some disadvantages."
    
    url = "https://provisionspall-hwvs.onrender.com/dashboard"
    html_content = f"""<html>
<body>
    <h1 style="color: blue;">Delivery - Business Application</h1>
    <br>
    <p>Copy this token and paste it in the
        <a href={url}>reset password page</a></p>
    <code>{mess}</code>
    <h1>OR</h1>
    <p>Directly update your password <a href="{url}?token={mess}">here</a>.</p>
</body>
</html>
"""
    message.attach(MIMEText(html_content, "html"))

    # Send the email
    await send_mail(sen, pas, addr, port, rec, message.as_string())
