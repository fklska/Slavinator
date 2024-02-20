import os

import base_classes
import excel
from dotenv import load_dotenv
from telegram import (File, InlineKeyboardButton, InlineKeyboardMarkup,
                      Update)
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ContextTypes,
                          MessageHandler, filters)

load_dotenv()

check_mail = base_classes.Email()
check_excel = excel.Excel()


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_html(
        f'{update.effective_user.first_name} <code> Hello world! </code>.',
    )

    await commands(update, context)


async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Отправить email", callback_data='email')
        ],
        [
            InlineKeyboardButton(
                "Написать Проводки в Excel",
                callback_data='excel'
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Доступные команды",
        reply_markup=reply_markup
    )


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data == 'email':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Введи email адрес"
        )
        await query.answer(text="Введи email адрес")
        check_mail.bool = True

    if query.data == 'excel':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Привет, это бот который будет помогать тебе делать задачи по бух учету \nТебе нужно отправить данные в excel таблице чтобы бот смог их проанализировать \nВот пример: ',
        )
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=open('v1/excel/template.xlsx', 'rb'),
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Есть несколько важных особенностей: \n 1) Счета и суммы отделяй пробелом \n 2) Новый счет/новая проводка = новая строчка \n 3) Если Excel сам форматирует числа и удаляет пробелы между ними ставь ' перед данными \n 4) Бот начинает читать файл со 2 строчки \n 5) Про активно-пассивные счета: такие счета считаются сразу для двух сторон как активный, так и пассивный. Если в вашем случае он пассивный значит ваша колонка кредита. Если а-п счет указывается в начальном балансе 2 раза он считается с двумя Сн",
        )
        await query.answer(text='Скинь файл excel')
        check_excel.bool = True

    #await query.answer(text=query.data)


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


async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if check_excel.bool:
        file = await update.message.document.get_file()
        await File.download_to_drive(
            file,
            custom_path='v1/excel/example.xlsx'
        )

        await update.message.reply_text(
            text='Файл получен'
        )

        print(f'Сообщение отправлено for User: {update.effective_user.username}, В чат: {update.effective_chat.id}')
        read_data = check_excel.read_excel()
        check_excel.create_excel(
            check_excel.account_entires(
                read_data['Wire'],
                check_excel.create_account(
                    read_data['Wire'],
                    read_data['Start']
                )
            )
        )

        await update.message.reply_document(
            document=open('v1/excel/sample.xlsx', 'rb')
        )
        check_excel.bool = False
    else:
        await update.message.reply_text(
            text='Нажми на inline кнопку, если ее нет введи /start'
        )


def main():
    app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    app.add_handler(CommandHandler("start", hello))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(MessageHandler(filters.Document.ALL, get_file))
    app.add_handler(MessageHandler(None, workflow))

    app.run_polling()


if __name__ == "__main__":
    main()
