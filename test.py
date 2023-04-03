import account

test1 = account.Account(50)
test1.get_debet(1, 1500)
test1.get_debet(2, 5500)
test1.get_credit(6, 55000)

test1.get_gross_credit()
test1.get_gross_debet()

test2 = account.Account(50)
test2.get_debet(1, 10500)
test2.get_debet(2, 5500)
test2.get_credit(8, 55000)

test2.get_gross_credit()
test2.get_gross_debet()

print(test1)
print(test2)