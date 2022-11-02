from datetime import datetime

class Reminder:
    def __init__(self):
        self.s = 10

    def remind(self):
        if datetime.now().second % self.s == 0:
            print(self.s)
            self.s += 5

proc = Reminder()

while True:
    proc.remind()
