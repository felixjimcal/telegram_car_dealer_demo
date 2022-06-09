from telegram import Update
from telegram.ext import CallbackContext

from utils import *


class Locater:
    @staticmethod
    async def location_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
        try:
            text = "Puedes encontrarnos en:" + "\n" + "\n"
            text += "📍" + " " + "Pl. de la Independencia, s/n, 28001 Madrid" + "\n"
            text += "<a href='https://www.google.com/maps/place/Puerta+de+Alcal%C3%A1/@40.419992,-3.688737,17z/data=!3m1!4b1!4m5!3m4!1s0xd42289a4a865227:0x98278b3a144a86f1!8m2!3d40.419992!4d-3.688737'>🗺️ Google Maps</a>" + '\n'
            await update.message.reply_html(text)

            lat = 40.419992
            lon = -3.688737
            await update.message.reply_location(lat, lon)
        except Exception as ex:
            error_message(ex)
