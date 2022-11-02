from mongo import Mongo
from table import Sheet

def is_registered(id, last_name):
    res = Mongo.find(last_name)
    if res is None:
        register(id, last_name)
        return True
    else:
        return True

def register(id, last_name):
    usr = {'_id': id, 'last_name': last_name}
    Mongo.add_new(usr)

def wrong_cmd(vk_session, id):
    msg = 'Я таких слов не знаю :(\nДля списка команд введи "помощь"'
    vk_session.method('messages.send', {"user_id": id, "message": msg, "random_id": 0})

def help(vk_session, id, last_name):
    msg = "Список команд:\nПомощь\nБабло"
    vk_session.method('messages.send', {"user_id": id, "message": msg, "random_id": 0})

def payment_amount(vk_session, id, last_name):
    sum = Sheet.payment_amount(last_name)
    if sum == -1:
        msg = "Хто ты?"
    else:
        msg = f"Вы внесли {sum} рублей из 15"
    vk_session.method('messages.send', {"user_id": id, "message": msg, "random_id": 0})
