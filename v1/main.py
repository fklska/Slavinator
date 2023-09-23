from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler
from dotenv import load_dotenv
import os
import base_classes

load_dotenv()

check_mail = base_classes.Email()


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}'
    )

    await commands(update, context)


async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Отправить email", callback_data='email'),
            InlineKeyboardButton("Option 2 in line 1", callback_data=2)
        ],
        [InlineKeyboardButton("Option 3 line 2", callback_data=3)],
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


def main():
    app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    app.add_handler(CommandHandler("start", hello))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(MessageHandler(None, workflow))

    app.run_polling()


if __name__ == "__main__":
    main()
