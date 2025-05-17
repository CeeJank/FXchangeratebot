import asyncio
import os 
import telegram
from dotenv import load_dotenv
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, Application, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler

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
        [
            # row 1
            InlineKeyboardButton("USD", callback_data="1"),
            InlineKeyboardButton("SGD", callback_data="2"),
        ],
        # row 2
        [InlineKeyboardButton("MYR", callback_data="3")],
    ]
    # turns list into actual inlinekeyboard
    reply_markup = InlineKeyboardMarkup(keyboard)

    # await tells program to stop and wait for function call to finish
    await update.message.reply_text("Please Choose", reply_markup=reply_markup)



# actual buttons of the keyboard
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # access to the provided CallbackQuery
    query = update.callback_query

    # answers the callbackquery
    await query.answer()

    # edits the message where CallbackQuery comes from, then inserts data defined in keyboard(1,2,3)
    # doesn't pass the inline keyboard again
    await query.edit_message_text(text=f"You have chosen {query.data}")

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
    