import random

from telegram import KeyboardButton, LabeledPrice, ReplyKeyboardMarkup, Update, WebAppInfo
from telegram.ext import CallbackContext

from secret_files import pass_keys
from utils import *


class Shoper:
    @staticmethod
    async def shop_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
        try:
            message_text = "Presiona en el comando para acceder a nuestro servicio web. 👇" + "\n"
            await update.message.reply_text(
                text=message_text,
                reply_markup=ReplyKeyboardMarkup.from_button(
                    KeyboardButton(
                        text="Merchandise 🛒",
                        web_app=WebAppInfo(url='https://equistebbot.herokuapp.com/shop.html'),
                    )
                ),
            )
        except Exception as ex:
            error_message(ex)

    @staticmethod
    async def pre_checkout_callback(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
        await Shoper.check_payload(update)

    @staticmethod
    async def successful_payment_callback(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
        await Shoper.send_successful_payment_message(update)

    @staticmethod
    async def send_invoice(update, context, json_reply):
        try:
            json_reply = json_reply['shop']
            product_name = json_reply['product']
            product_price = json_reply['price']
            product_amount = json_reply['amount']

            chat_id = update.message.chat_id
            title = 'Order #' + str(random.randint(1, 9999))
            description = "Pedido en web app"
            payload = "Custom-Payload"  # select a payload just for you to recognize its the donation from your bot
            currency = "EUR"  # check https://core.telegram.org/bots/payments#supported-currencies for more details
            price = str(product_price).replace('.', '')
            prices = [LabeledPrice(product_name, price)]

            message_fake_invoice = 'Tu <b>factura demo</b> está lista. Para pagar tu pedido ficticio, usa este número de tarjeta <code>4242 4242 4242 4242</code>, puedes utilizar cualquier la fecha de caducidad, en el futuro, y cualquier número como CVV.'
            await update.message.reply_html(text=message_fake_invoice)

            resume_invoice = "Artículos:" + " \n" + " \n"
            resume_invoice += product_name + " x " + str(product_amount) + ": " + str(product_price) + "€ \n\n"
            resume_invoice += "Total: <b>" + str(product_price) + "€</b>"
            await update.message.reply_html(text=resume_invoice)

            await context.bot.send_invoice(
                chat_id,
                title,
                description,
                payload,
                pass_keys.STRIPE_TEST_TOKEN,  # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
                currency,
                prices,
                need_name=True,  # optional
                need_phone_number=True,  # optional
                need_email=True,  # optional
                need_shipping_address=False,  # optional
                is_flexible=False,  # Price changes when need_shipping_address is True
                photo_url="https://cdn4.iconfinder.com/data/icons/shopping-376/100/shopping-bag-2-shopping-bags-tag-512.png",
                photo_width=5,
                photo_height=5
            )
        except Exception as ex:
            error_message(ex)

    @staticmethod
    async def check_payload(update):
        try:
            query = update.pre_checkout_query
            # check the payload, is this from your bot?
            if query.invoice_payload != "Custom-Payload":
                # answer False pre_checkout_query
                await query.answer(ok=False, error_message="Something went wrong...")
            else:
                await query.answer(ok=True)
        except Exception as ex:
            error_message(ex)

    @staticmethod
    async def send_successful_payment_message(update):
        await update.message.reply_text("Thank you for your payment!")
