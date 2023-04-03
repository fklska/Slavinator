class Account():

    def __init__(self, number, opening_balance=0) -> None:
        self.number = number
        self.credit = {

        }
        self.debet = {

        }
        self.gross_debet = 0
        self.gross_credit = 0

        self.opening_balance = opening_balance
        self.closing_balance = 0

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
        self.closing_balance = int(self.opening_balance) + self.gross_debet - self.gross_credit

    def __str__(self) -> str:
        return (
            f'Счет {self.number} \n Операции по Дебету: {self.debet} \n'
            f' Операции по Кредиту: {self.credit} \n'
            f' Оборот по дебету: {self.gross_debet} \n'
            f' Оборот по кредиту: {self.gross_credit} \n'
        )
