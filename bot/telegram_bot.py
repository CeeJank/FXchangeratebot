import asyncio
import os 
import telegram
from dotenv import load_dotenv
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, Application, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler
from exchangerate.exchange_rate import commonCurrencies
from exchangerate.exchange_rate import moreCurrencies



# logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

# fetch api key
load_dotenv()
token = os.environ.get("TG_TOKEN_API")

# inline keyboard markups
async def rates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 2D-matrix 
    keyboard = [
            # row 1
            [InlineKeyboardButton(currency, callback_data=f"{currency}") for currency in commonCurrencies()],
            #row 2
            [InlineKeyboardButton("More Currencies", callback_data="more")]
    ]

    # turns list into actual inlinekeyboard
    reply_markup = InlineKeyboardMarkup(keyboard)

    # await tells program to stop and wait for function call to finish
    await update.message.reply_text("Please Choose", reply_markup=reply_markup)


# buttons handler of the keyboard
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # access to the provided CallbackQuery
    query = update.callback_query

    # acknowledges the button press
    await query.answer()

    data = query.data

    # edits the message where CallbackQuery comes from, then inserts data defined in keyboard
    # pass the inline keyboard again only with reply_markup
    await query.edit_message_text(text=f"You have chosen {query.data}", reply_markup=InlineKeyboardMarkup([InlineKeyboardButton("rates", callback_data="rates")]))

    if data == "more":
        await more(update, context)
    elif data == "reset":
        await reset(update, context)


async def more(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:

    keyboard = [
        [InlineKeyboardMarkup(callback_data=f"{more}")] for more in moreCurrencies()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text


async def reset() -> None: 
    return



# help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Use /rates to initialize")

# initialize bot
def buildBot():
    # fetch/handle updates from the update_queue
    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("rates", rates))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    # continuously makes request to tg servers for updates
    application.run_polling()
    