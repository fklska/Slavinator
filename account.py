class Account():
    ACTIVE = ["1", "3", "4", "7", "8", "9", "10", "11", "19", "20", "21", "23", "25", "26", "28", "29", "41", "43", "44", "45", "46", "50", "51", "52", "55", "57", "58", "81", "94", "97"]
    PASSIVE = ["2", "5", "42", "59", "63", "66", "67", "70", "77", "80", "82", "83", "96", "98"]
    ACTIVE_PASSIVE = ["14", "15", "16", "40", "60", "62", "68", "69", "71", "73", "75", "76", "79", "84", "86", "90", "91", "99"]

    def __init__(self, number, opening_balance=0, opening_balance_credit=0, status=None, double=False) -> None:
        self.number = number
        self.credit = {

        }
        self.debet = {

        }
        self.gross_debet = 0
        self.gross_credit = 0

        self.opening_balance = int(opening_balance)
        self.opening_balance_credit = int(opening_balance_credit)

        self.closing_balance_debet = 0
        self.closing_balance_credit = 0
        self.closing_balance = 0

        self.status = status
        self.double = double

    def get_status(self):
        if self.status is None:
            if self.number in self.ACTIVE:
                self.status = 'Active'

            if self.number in self.PASSIVE:
                self.status = 'Passive'

            if self.number in self.ACTIVE_PASSIVE:
                self.status = 'Act_Pass'

    def get_debet(self, operation_number, summ):
        self.debet[operation_number] = summ

    def get_credit(self, operation_number, summ):
        self.credit[operation_number] = summ

    def get_gross_debet(self):
        summ = 0
        for i in self.debet:
            summ = summ + int(self.debet[i])
        self.gross_debet = summ

    def get_gross_credit(self):
        summ = 0
        for i in self.credit:
            summ = summ + int(self.credit[i])
        self.gross_credit = summ

    def get_closing_saldo(self):
        if self.status == 'Active':
            self.closing_balance = self.opening_balance + self.gross_debet - self.gross_credit

        elif self.status == 'Passive':
            self.closing_balance = self.opening_balance - self.gross_debet + self.gross_credit

        elif self.double:
            self.closing_balance_debet = self.opening_balance + self.gross_debet - self.gross_credit
            self.closing_balance_credit = self.opening_balance_credit - self.gross_debet + self.gross_credit
        else:
            self.closing_balance_debet = self.opening_balance + self.gross_debet - self.gross_credit
            self.closing_balance_credit = self.opening_balance - self.gross_debet + self.gross_credit

    def __str__(self) -> str:
        return (
            f'Счет {self.number} \n Операции по Дебету: {self.debet} \n'
            f' Операции по Кредиту: {self.credit} \n'
            f' Оборот по дебету: {self.gross_debet} \n'
            f' Оборот по кредиту: {self.gross_credit} \n'
        )
