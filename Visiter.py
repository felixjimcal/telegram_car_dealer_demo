from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from Emailer import *
from utils import *


class Visiter:
    @staticmethod
    async def visit_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
        try:
            message_text = "Presiona en el comando para acceder a nuestro servicio web. 👇" + "\n"
            await update.message.reply_text(
                text=message_text,
                reply_markup=ReplyKeyboardMarkup.from_button(
                    KeyboardButton(
                        text="Agendar visita 📅",
                        web_app=WebAppInfo(url='https://equistebbot.herokuapp.com/'),
                    )
                ),
            )
        except Exception as ex:
            error_message(ex)

    @staticmethod
    async def make_appointment(data, update):
        try:
            data = data['visit']
            contact = Contact(data['name'], data['phone'], data['email'], data['day'], data['time'], '')
            contact.visit_location = 'https://www.google.com/maps/place/Puerta+de+Alcal%C3%A1/@40.419992,-3.688737,17z/data=!3m1!4b1!4m5!3m4!1s0xd42289a4a865227:0x98278b3a144a86f1!8m2!3d40.419992!4d-3.688737'
            Emailer.send_visit_email(contact)
            text = "🎉 Perfecto! Hemos recibido tu solicitud.\n" + "\n"
            text += "En breve nos pondremos en contacto contigo." + "\n"
            text += "Revisa tu correo electrónico  y carpeta de SPAM: \n"
            text += "<code>" + contact.email + "</code>" + "\n" + "\n"
            text += "¡Gracias por confiar en nosotros! :)" + "\n"
            await update.message.reply_html(text=text, reply_markup=ReplyKeyboardRemove())
        except Exception as ex:
            error_message(ex)
