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
    msg = "Список команд:\nПомощь\nБабло\nЧек"
    vk_session.method('messages.send', {"user_id": id, "message": msg, "random_id": 0})

def payment_amount(vk_session, id, last_name):
    sum = Sheet.payment_amount(last_name)
    if sum == -1:
        msg = "Хто ты?"
    else:
        msg = f"Вы внесли {sum} рублей из 15"
    vk_session.method('messages.send', {"user_id": id, "message": msg, "random_id": 0})

def notification(vk_session, id, last_name):
    for boets in Sheet.boets_list():
        if Mongo.find(boets) is None:
            msg = f'{boets}  - гомосексуалист, т.к. еще не зарегистрировался в боте'
            vk_session.method('messages.send', {"user_id": 162267140, "message": msg, "random_id": 0})
        else:
            sum = Sheet.payment_amount(boets)
            if sum == -1:
                msg = f'Чувырло по имени {boets} еще ничего не внес в кассу!!!'
                vk_session.method('messages.send', {"user_id": 162267140, "message": msg, "random_id": 0})
            elif sum == 15:
                msg = f'Ну {boets} же просто зайка! Все деньги внесены!'
                vk_session.method('messages.send', {"user_id": 162267140, "message": msg, "random_id": 0})
            else:
                msg = f'Когда {boets} докинет еще {15 - sum}, то будет ваще кучеряво'
                vk_session.method('messages.send', {"user_id": 162267140, "message": msg, "random_id": 0})

def deposit(vk_session, id, last_name):
    msg = f'{last_name} говорит, что внес копеечку в кассу'
    vk_session.method('messages.send', {"user_id": 162267140, "message": msg, "random_id": 0})
