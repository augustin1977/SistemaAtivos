import smtplib
from email.mime.text import MIMEText
from cadastro_equipamentos import settings
from usuarios.models import *
import threading
def enviar_email(subject,body,recipients):
        html_message = MIMEText(body, 'html')
        html_message['Subject'] = subject
        html_message['From'] = settings.EMAIL_HOST_USER
        html_message['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, recipients, html_message.as_string())   

def enviar_email_background(subject, body, recipients):
    def send():
        try:
            html_message = MIMEText(body, 'html')
            html_message['Subject'] = subject
            html_message['From'] = settings.EMAIL_HOST_USER
            html_message['To'] = ', '.join(recipients)
            with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(settings.EMAIL_HOST_USER, recipients, html_message.as_string())
        except Exception as e:
            pass

    # Cria e inicia a thread
    thread = threading.Thread(target=send)
    thread.start()
