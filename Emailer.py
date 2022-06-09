from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils import *
from secret_files import pass_keys
import smtplib

FIT_BOT_EMAIL = 'fitbotweb@gmail.com'


class Emailer:
    @staticmethod
    def send_visit_email(contact):
        try:
            sender_address = FIT_BOT_EMAIL
            sender_pass = pass_keys.FIT_BOT_EMAIL_PWD
            receiver_address = contact.email
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'Visita CarDealer'

            # The body and the attachments for the mail
            email_text = "Hola, " + contact.name + "!\n\n"
            email_text += "Te enviamos este email conforme has agendado una visita en nuestro centro.\n"
            email_text += "Te recordamos los detalles de la visita:\n\n"
            email_text += "Fecha: " + contact.day + "\n"
            email_text += "Hora: " + contact.time + "\n"
            email_text += "Dirección: " + contact.visit_location + "\n"
            email_text += "\n\n"
            email_text += "Nos vemos!\n\n"
            message.attach(MIMEText(email_text, 'plain'))

            # Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
            session.ehlo()
            session.starttls()  # enable security
            session.ehlo()
            session.login(sender_address, sender_pass)  # login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
        except Exception as ex:
            error_message(ex)
