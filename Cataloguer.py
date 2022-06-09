from utils import *
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


class Cataloguer:
    @staticmethod
    async def catalogue_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
        try:
            keyboard = [
                [InlineKeyboardButton(text='2017 Huracán LP610-4 Avio', callback_data='2017_huracan_lp610_4_avio')],
                [InlineKeyboardButton(text='2016 Huracán LP610-4 Spyder', callback_data='2016_huracan_lp610_4_spyder')],
                [InlineKeyboardButton(text='2018 BMW M2', callback_data='2018_bmw_m2')],
                [InlineKeyboardButton(text='2021 Nissan GT-R', callback_data='2021_nissan_gt-r')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            text = "Selecciona un modelo:" + "\n"
            await update.message.reply_text(text, reply_markup=reply_markup)
        except Exception as ex:
            error_message(ex)

    @staticmethod
    async def catalogue_option(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
        try:
            query = update.callback_query
            doc = None
            if query.data == '2017_huracan_lp610_4_avio':
                doc = open('pdf/Lamborghini_int Huracan LP 610-4 Avio_2017.pdf', 'rb')
            elif query.data == '2016_huracan_lp610_4_spyder':
                doc = open('pdf/Lamborghini_int Huracan LP 610-4 Spyder_2016.pdf', 'rb')
            elif query.data == '2018_bmw_m2':
                doc = open('pdf/BMW_US M2_2018.pdf', 'rb')
            elif query.data == '2021_nissan_gt-r':
                doc = open('pdf/Nissan_US GT-R_2021.pdf', 'rb')
            await query.edit_message_text(text='Preparando... ⌛')
            await query.message.reply_document(doc)
        except Exception as ex:
            error_message(ex)
