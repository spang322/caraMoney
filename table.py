import gspread

class Sheet:
    def __init__(self):
        self.sa = gspread.service_account()
        self.sh = self.sa.open("Квартирник")

        self.wks = self.sh.worksheet("Лист1")

