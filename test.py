from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append()
wb.save('Test.xlsx')
