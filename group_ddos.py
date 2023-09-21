from telegram import Bot
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))


def main():
    for i in range(5):
        bot.send_message(
            chat_id='-4063108632',
            text=f'{i} Ddos attack'
        )
        sleep(0.5)


if __name__ == '__main__':
    main()
