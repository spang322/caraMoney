import gspread


class Sheet:
    def __init__(self):
        self.sa = gspread.service_account()
        self.sh = self.sa.open("Квартирник")

        self.wks = self.sh.worksheet("Лист2")

    def payment_amount(self, last_name):
        last_name_list = [i[0] for i in self.wks.get('A1:A5')]

        if last_name in last_name_list:
            num = last_name_list.index(last_name) + 1
        else:
            return -1

        payment_list = [list(filter(None, i)) for i in self.wks.get(f'B{num}:D{num}')][0]
        if payment_list:
            return sum([int(i) for i in payment_list])
        else:
            return -1

    def boets_list(self):
        i = 1
        boets_list = []

        while True:
            boets = self.wks.acell(f'A{i}').value
            print(boets)
            if boets is None:
                break
            boets_list.append(boets)
            i += 1

        return boets_list

    def cell_int_value(self, cell_id):
        return int(self.wks.acell(cell_id).value)


Sheet = Sheet()
