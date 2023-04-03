import requests
from telegram import ReplyKeyboardMarkup, Bot, File
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters
from account import Account
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Border, NamedStyle, Side, Alignment
import logging

updater = Updater(token='5931393528:AAGAWkOyIURPzq-BKHr7HDutyqWtxZdThQw')
URL = 'https://api.thecatapi.com/v1/images/search'

logging.basicConfig(
    filemode='w',
    filename='main.log',
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(message)s'
)
logger = logging.getLogger(__name__)


def text_format(text):
    dic = {

    }
    for i in range(len(text.split(';'))):
        dic[i] = text.split(';')[i]  
    return dic


def create_account(dic, start_dic):
    numbers = []
    accounts = []
    for value in dic.values():
        numbers.append(value.split(' ')[0])
        numbers.append(value.split(' ')[1])

    numbers = list(set(numbers))

    for value in start_dic.values():
        accounts.append(Account(number=value.split(' ')[0], opening_balance=value.split(' ')[1]))
        if value.split(' ')[0] in numbers:
            numbers.remove(value.split(' ')[0])

    for number in numbers:
        accounts.append(Account(number))

    return accounts


def account_entires(dic, accounts):
    count = 0
    for wire in dic.values():
        array = wire.split(' ')
        for acc in accounts:
            try:
                if array[0] == acc.number:
                    acc.get_debet(count, array[2])
                if array[1] == acc.number:
                    acc.get_credit(count, array[2])
            except IndexError:
                return 'Введи нормальные данные'
        count += 1
    for acc in accounts:
        acc.get_gross_debet()
        acc.get_gross_credit()
        acc.get_closing_saldo()
    return accounts


def get_codes(update, context):
    chat = update.effective_chat
    create_excel(account_entires(text_format(update.message.text), create_account(text_format(update.message.text),{})))
    context.bot.send_document(
        chat_id=chat.id,
        document=open('sample.xlsx', 'rb'),
    )


def read_excel():
    wb = load_workbook('example.xlsx')
    ws = wb.active
    data = {
        "Start": {

        },
        "Wire": {

        },
    }

    for row in range(1, 100):
        if ws[f'A{row}'].value is not None:
            data["Start"][row] = ws[f'A{row}'].value

    for row in range(1, 100):
        if ws[f'B{row}'].value is not None:
            data["Wire"][row] = ws[f'B{row}'].value
    return data


def show_message(accounts):
    message = ''
    for i in accounts:
        message += str(i)
    return message


bottom_border = Border(bottom=Side(style='medium'))
right_border = Border(right=Side(style='medium'))
left_border = Border(left=Side(style='medium'))
top_border = Border(top=Side(style='medium'))


def create_excel(datas):
    wb = Workbook()
    ws = wb.active
    col = 1
    row = 3
    for data in datas:
        #print(data)

        ws.merge_cells(f'{ws.cell(row=row-2, column=col).coordinate}:{ws.cell(row=row-2, column=col+1).coordinate}')

        ws.cell(row=row-2, column=col).alignment = Alignment(horizontal='center', vertical='center')
        ws.cell(row=row-2, column=col).border = bottom_border
        ws.cell(row=row-2, column=col+1).border = bottom_border
        ws.cell(row=row-2, column=col).value = data.number
        ws.cell(row=row-1, column=col).border = Border(right=Side(style='medium'), bottom=Side(style='medium'))
        ws.cell(row=row-1, column=col+1).border = bottom_border
        ws.cell(row=row-1, column=col).value = f'Сн = {data.opening_balance}'

        count = 0
        for i in data.debet:

            ws.cell(row=row+count, column=col).border = right_border
            ws.cell(row=row+count, column=col).value = f'{i + 1}){data.debet[i]}'
            count += 1

        count = 0
        for i in data.credit:
            ws.cell(row=row+count, column=col+1).border = left_border
            ws.cell(row=row+count, column=col+1).value = f'{i + 1}){data.credit[i]}'
            count += 1

        if not data.debet and not data.credit:
            ws.cell(row=row, column=col).border = right_border
            ws.cell(row=row+1, column=col).border = Border(top=Side(style='medium'), bottom=Side(style='medium'), right=Side(style='medium'))
            ws.cell(row=row+1, column=col+1).border = Border(top=Side(style='medium'), bottom=Side(style='medium'))

            ws.cell(row=row+1, column=col).value = f'Обд = {data.gross_debet}'
            ws.cell(row=row+1, column=col+1).value = f'Обк = {data.gross_credit}'

            ws.cell(row=row+2, column=col).value = f'Ск = {data.closing_balance}'
        else:
            if len(data.debet) > len(data.credit):
                ws.cell(row=row+len(data.debet), column=col).border = right_border
                ws.cell(row=row+len(data.debet), column=col).border = Border(top=Side(style='medium'), bottom=Side(style='medium'), right=Side(style='medium'))
                ws.cell(row=row+len(data.debet), column=col+1).border = Border(top=Side(style='medium'), bottom=Side(style='medium'))

                ws.cell(row=row+len(data.debet), column=col).value = f'Обд = {data.gross_debet}'
                ws.cell(row=row+len(data.debet), column=col+1).value = f'Обк = {data.gross_credit}'

                ws.cell(row=row+len(data.debet) + 1, column=col).value = f'Ск = {data.closing_balance}'
            else:
                ws.cell(row=row+len(data.credit), column=col).border = Border(top=Side(style='medium'), bottom=Side(style='medium'), right=Side(style='medium'))
                ws.cell(row=row+len(data.credit), column=col+1).border = Border(top=Side(style='medium'), bottom=Side(style='medium'))

                ws.cell(row=row+len(data.credit), column=col).value = f'Обд = {data.gross_debet}'
                ws.cell(row=row+len(data.credit), column=col+1).value = f'Обк = {data.gross_credit}'

                ws.cell(row=row+len(data.credit) + 1, column=col).value = f'Ск = {data.closing_balance}'

        col += 3
        if col > 7:
            row += 7
            col = 1
    wb.save("sample.xlsx")


def get_file(update, context):
    chat = update.effective_chat
    file = context.bot.get_file(
        update.message.document.file_id
    )
    File.download(
        file,
        custom_path='example.xlsx')
    context.bot.send_message(
        chat_id=chat.id,
        text='Файл получен',
    )

    print(f'Сообщение отправлено for User: {update.effective_user}, В чат: {update.effective_chat}')

    create_excel(account_entires(read_excel()['Wire'], create_account(read_excel()['Wire'], read_excel()['Start'])))
    context.bot.send_document(
        chat_id=chat.id,
        document=open('sample.xlsx', 'rb'),
    )


text = "10 20 500;50 51 5500;51 80 5100;70 51 5100;10 20 999;40 41 650;72 73 870"


def main():
    
    #create_excel(account_entires(read_excel()['Wire'], create_account(read_excel()['Wire'], read_excel()['Start'])))

    updater.dispatcher.add_handler(MessageHandler(Filters.document, get_file))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, get_codes))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
