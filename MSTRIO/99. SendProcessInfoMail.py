from Constants import *
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

receiver_email = "michael.hoffmann@naturaktiverleben.de"
subject = "Message from Python Code"
body = "This is an email test from Python.\n\nHello World!\nHello Team!"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))
text = message.as_string()

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, text)
    server.quit()
    print('Mail sent')