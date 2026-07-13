import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from config import Config

def send_email(to, subject, html_body):
    msg = MIMEMultipart("alternative")
    
    msg["Subject"] = subject
    msg["From"] = Config.MAIL_DEFAULT_SENDER
    msg["To"] = to
    
    msg.attach(MIMEText(html_body, "html"))
    
    with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
        server.sendmail(Config.MAIL_DEFAULT_SENDER, to, msg.as_string())
        
def send_email_with_attachment(to, subject, html_body, attachment_data, attachment_name):       
    msg = MIMEMultipart("mixed")
    
    msg["Subject"] = subject
    msg["From"] = Config.MAIL_DEFAULT_SENDER
    msg["To"] = to
    
    
    msg.attach(MIMEText(html_body, "html"))
    
    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(attachment_data)
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=attachment_name)
    
    msg.attach(attachment)
    
    with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
        server.sendmail(Config.MAIL_DEFAULT_SENDER, to, msg.as_string())
    
