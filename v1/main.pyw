from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputTextMessageContent, InlineQuery, Invoice, LabeledPrice, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, InlineQueryHandler, filters
from dotenv import load_dotenv
import os
import base_classes
from uuid import uuid4
from html import escape
from telegram.constants import ParseMode
import json

load_dotenv()

check_mail = base_classes.Email()


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}',

    )

    await update.message.reply_html(
        "<code> Pick color test_code</code>.",
    )

    await update.message.reply_invoice(
        title='Test',
        description='ge',
        start_parameter='testStartParam',
        payload='test',
        provider_token='381764678:TEST:67421',
        currency='RUB',
        prices=[LabeledPrice('str', 100 * 100), ],
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Оплатить', pay=True)]]),

    )
    await commands(update, context)


async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Отправить email", callback_data='email'),
            InlineKeyboardButton("Option 2 in line 1", web_app=WebAppInfo('https://github.com/fklska'))
        ],
        [InlineKeyboardButton("Option 3 line 2", web_app=WebAppInfo("https://python-telegram-bot.org/static/webappbot"))],

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Доступные команды", reply_markup=reply_markup)


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data == 'email':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Введи email адрес"
        )
        await query.answer(text="Введи email адрес")
        check_mail.bool = True

    if query.data == 2:
        await query.answer(text='Test')

    await query.answer(text=query.data)


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query

    if not query:
        return

    if '.com' not in query:
        return

    results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Caps",
                input_message_content=InputTextMessageContent(query.upper()),
            ),

            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Paste URL button",
                input_message_content=InputTextMessageContent(query.split('!')[0]),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(query.split('!')[0], url=query.split('!')[1])]]),
            ),

        ]

    await update.inline_query.answer(results)


async def workflow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if check_mail.bool:
        if check_mail.adress is not None:

            check_mail.message = update.effective_message.text
            check_mail.send_mail()
            await update.message.reply_text("Письмо отправлено!")
            check_mail.bool = False
            await commands(update, context)

        else:
            check_mail.adress = update.effective_message.text
            print(check_mail)
            await update.message.reply_text("Введите текст:")


async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the received data and remove the button."""
    # Here we use `json.loads`, since the WebApp sends the data JSON serialized string
    # (see webappbot.html)
    print(update.effective_message.web_app_data)
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_html(
        f'<code>{data}</code>'
    )


def main():
    app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    app.add_handler(CommandHandler("start", hello))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    app.add_handler(MessageHandler(None, workflow))
    app.add_handler(InlineQueryHandler(inline_query))

    app.run_polling()


if __name__ == "__main__":
    main()
