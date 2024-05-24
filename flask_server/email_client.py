import smtplib
import os
from time import sleep
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio


async def mailSender(id=None, subj=None, mess=None, addr="smtp.gmail.com", pas=None, 
               sen=None, rec=None, port=465):
    if (sen is None or rec is None):
        return
    x = 0
    # load environmental variables
    load_dotenv()

    # get the environmental variable which has the password or use argument password
    if (pas is None):
        pas = os.getenv("GTP")

    # Prepare the message
    message = MIMEMultipart()
    message['From'] = sen
    message['To'] = rec
    if subj is None:
        message['Subject'] = "Email communication"
    else:
        message["Subject"] = subj
    if mess is None:
        mess = " Software engineering is good, but also has some disadvantage."
    # message.attach(MIMEText(mess, "plain"))
    url = "https://provisionspall-hwvs.onrender.com/dashboard"
    html_content = f"""<html>
<body>
    <h1 style="color: blue;">Delivery - Business Application</h1>
    <br>
    <p>Copy this token and paste it in the
        <a href={url}> reset password page </a></p>
    <code>{mess}</code>
    <h1>OR</h1>
    <p>Directly update your password <a href="{url}?token={mess}"> here</a>.</p>
</body>
</html>
"""
    message.attach(MIMEText(html_content, "html"))

    while (x < 7):
        # loop 7 times until mail is sent the mail
        
        try:
            # create the server
            server = smtplib.SMTP_SSL(addr, port)
            server.login(sen, pas)
            server.sendmail(sen, rec, message.as_string())
        except Exception as e:
            print(f"error:{str(e)}")
            print("Please wait, retrying ...")
            await asyncio.sleep(2)
        else:
            print("mail sent!")
            if (server):
                server.quit()
            break
        finally:
            print("Success 😎")
        x += 1

# test me
if __name__ == '__main__':
    mailSender(sen="chinonsodomnic@gmail.com", rec="dominicmorba@gmail.com", pas=None)