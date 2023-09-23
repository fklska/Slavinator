from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ContextTypes, Application, CallbackQueryHandler
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

#updater = Updater(token=os.getenv('TOKEN'))

keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
            InlineKeyboardButton("Option 3", callback_data="3"),
        ],
        [InlineKeyboardButton("Option 4", callback_data="4")],
    ]
reply_markup = InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        'Please chose',
        reply_markup=reply_markup
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    print(query.data)
    await query.edit_message_text(text=f"Current Selected option: {query.data}", reply_markup=reply_markup)


def main():
    application = Application.builder().token(os.getenv('TOKEN')).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
