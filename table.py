import gspread


class Sheet:
    def __init__(self):
        self.sa = gspread.service_account()
        self.sh = self.sa.open("Квартирник")

        self.wks = self.sh.worksheet("Лист2")

    def payment_amount(self, last_name, boets_amount):
        last_name_list = [i[0] for i in self.wks.get(f'A1:A{boets_amount}')]  # CHANGE TO A2 AFTER SWAP

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
            if boets is None:
                break
            boets_list.append(boets)
            i += 1

        return boets_list

    def add_money(self, row_num, deposit, deposit_per_month):
        columns_list = ['B', 'C', 'D', 'F']

        for i in columns_list:
            current_sum = self.wks.acell(f'{i}{row_num}').value
            if current_sum is None:
                current_sum = 0
            else:
                current_sum = int(current_sum)

            if current_sum < deposit_per_month:
                delta = deposit - (deposit_per_month - current_sum)

                if delta > 0:
                    self.wks.update(f'{i}{row_num}', deposit_per_month)
                    deposit -= deposit_per_month - current_sum
                else:
                    self.wks.update(f'{i}{row_num}', current_sum + deposit)
                    return 0

        return deposit

    def cell_int_value(self, cell_id):
        return int(self.wks.acell(cell_id).value)


Sheet = Sheet()
