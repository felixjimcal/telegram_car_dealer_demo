import datetime
import json

from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, PreCheckoutQueryHandler

from Cataloguer import *
from Locater import *
from Shoper import Shoper
from Visiter import *
from secret_files import pass_keys
from utils import *


async def start_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    try:
        print(update.effective_user.first_name, "pressed /start", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        text = "Hola, " + update.effective_user.first_name + "! 👋" + "\n"
        text += "\n"
        text += "En que puedo ayudarte?" + "\n"
        # text += "/idioma " + " " + "change language" + " 🇪🇸🇬🇧🇩🇪" + "\n"
        text += "/ubicacion" + " " + "Ver donde estamos" + " 📍" + "\n"
        text += "/visita" + " " + "Agenda una reunión en nuestras oficinas" + " 📅" + "\n"
        text += "/catalogo" + " " + "Conoce nuestro stock" + " 🔖" + "\n"
        # text += "/notificaciones" + " " + "No te pierdas nuestras novedaes" + " 🔔" + "\n"
        text += "/tienda" + " " + "Descubre nuestro merchandise" + " 🏪" + "\n"
        await update.message.reply_text(text)
    except Exception as ex:
        error_message(ex)


async def web_app_reply(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    try:
        data = json.loads(update.effective_message.web_app_data.data)
        if data['webapp'] == 'visit':
            await Visiter.make_appointment(data, update)
        elif data['webapp'] == 'shop':
            await Shoper.send_invoice(update, context, data)
    except Exception as ex:
        error_message(ex)


def main() -> None:
    application = Application.builder().token(pass_keys.TELEGRAM_PRODUCTION_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ubicacion", Locater.location_command))

    application.add_handler(CommandHandler("visita", Visiter.visit_command))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_reply))

    application.add_handler(CommandHandler("tienda", Shoper.shop_command))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_reply))
    application.add_handler(PreCheckoutQueryHandler(Shoper.pre_checkout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, Shoper.successful_payment_callback))

    application.add_handler(CommandHandler("catalogo", Cataloguer.catalogue_command))
    application.add_handler(CallbackQueryHandler(Cataloguer.catalogue_option))

    application.run_polling()


if __name__ == "__main__":
    main()
