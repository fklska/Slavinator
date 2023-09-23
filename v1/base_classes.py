import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from dotenv import load_dotenv

load_dotenv()


class Email:
    def __init__(self) -> None:
        self.bool = False
        self.adress = None
        self.message = None

    def send_mail(self):
        msg = MIMEText(
            self.message,
            'plain',
            'utf-8'
        )
        msg['Subject'] = Header('Письмо от бота', 'utf-8')
        msg['From'] = os.getenv('LOGIN')
        msg['To'] = self.adress

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()
        s.login(os.getenv('LOGIN'), os.getenv('PASS'))
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()

    def __str__(self) -> str:
        return f'Письмо {self.bool} to {self.adress} with {self.message}'


if __name__ == "__main__":
    test_mail = Email()
    test_mail.bool = True
    test_mail.adress = 'slava111003@yandex.ru'
    test_mail.message = 'Письмо из кода'
    print(test_mail)
    test_mail.send_mail()
