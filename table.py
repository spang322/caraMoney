import gspread

sa = gspread.service_account()
sh = sa.open("Квартирник")

wks = sh.worksheet("Лист1")

print(wks.acell("B2").value)
