from mongo import Mongo
from table import Sheet
from datetime import datetime


def log(sender_id, msg, to_user):
    if to_user:
        sender_id = 0  # id = 0 is reserved by bot for logging

    Mongo.add_log(sender_id, msg, datetime.now())


def is_registered(user_id, last_name):
    res = Mongo.find_user(last_name)
    if res is None:
        register(user_id, last_name)
        return True
    else:
        return True


def register(user_id, last_name):
    Mongo.add_new(user_id, last_name)


def wrong_cmd(vk_session, user_id):
    msg = 'Я таких слов не знаю :(\nДля списка команд введи "помощь"'
    vk_session.method('messages.send', {"user_id": user_id, "message": msg, "random_id": 0})


def help_user(vk_session, user_id, last_name, user_msg):
    msg = """Список команд:
    \n"Помощь" - список команд
    \n"Бабло" - информация о внесенных средствах
    \n"Внес (сумма)" - уведомить коменданта, о том что ты внес деньги в кассу
    \n"Комендант" - призывает коменданта (опасно)"""

    if user_id == Sheet.cell_int_value('G1'):  # CHANGE AFTER SWAP
        msg += """"Чек" - напоминание полупокерам о том, что нужно внести бабло"""

    vk_session.method('messages.send', {"user_id": user_id, "message": msg, "random_id": 0})


def payment_amount(vk_session, user_id, last_name, user_msg):
    boets_amunt = len(Sheet.boets_list())
    pm_sum = Sheet.payment_amount(last_name, boets_amunt)
    if pm_sum == -1:
        msg = "Хто ты?"
    else:
        msg = f"Вы внесли {pm_sum} рублей из 15"
    vk_session.method('messages.send', {"user_id": user_id, "message": msg, "random_id": 0})


def notification(vk_session, user_id, last_name, user_msg):
    admin_id = Sheet.cell_int_value('G1')  # CHANGE AFTER SWAP

    if admin_id != user_id:
        msg = 'Ты как ваще эту команду узнал? Чеши отсюда, мамкин хакер...'
        vk_session.method('messages.send', {"user_id": user_id, "message": msg, "random_id": 0})
        return 0

    for boets in Sheet.boets_list():
        if Mongo.find(boets) is None:
            msg = f'{boets}  - гомосексуалист, т.к. еще не зарегистрировался в боте'
            vk_session.method('messages.send', {"user_id": admin_id, "message": msg, "random_id": 0})
        else:
            pm_sum = Sheet.payment_amount(boets)
            if pm_sum == -1:
                msg = f'Чувырло по имени {boets} еще ничего не внес в кассу!!!'
                vk_session.method('messages.send', {"user_id": admin_id, "message": msg, "random_id": 0})
            elif pm_sum == 15:
                msg = f'Ну {boets} же просто зайка! Все деньги внесены!'
                vk_session.method('messages.send', {"user_id": admin_id, "message": msg, "random_id": 0})
            else:
                msg = f'Когда {boets} докинет еще {15 - pm_sum}, то будет ваще кучеряво'
                vk_session.method('messages.send', {"user_id": admin_id, "message": msg, "random_id": 0})


def deposit(vk_session, user_id, last_name, user_msg):
    admin_id = Sheet.cell_int_value(cell_id='G1')  # CHANGE AFTER SWAP
    user_msg = user_msg.split()

    if len(user_msg) == 1:
        msg = 'Введите сумму, которую вы внесли'
        vk_session.method('messages.send', {"user_id": user_id, "message": msg, "random_id": 0})

    else:
        try:
            Mongo.add_deposit(user_id, last_name, int(user_msg[1]), datetime.now())

            msg = f'{last_name} говорит, что он внес {int(user_msg[1])}.' \
                  f'Чтобы подтвердить или отклонить перевод, напиши' \
                  f'"Пришло {last_name}" или "Не пришло {last_name}" соответственно'
            vk_session.method('messages.send', {"user_id": admin_id, "message": msg, "random_id": 0})

            msg = 'Спасибо! Уже написал коменданту :)'
            vk_session.method('messages.send', {"user_id": user_id, "message": msg, "random_id": 0})

        except Exception as e:
            print(e)
            msg = 'Сумма должна быть в циферках -_-'
            vk_session.method('messages.send', {"user_id": user_id, "message": msg, "random_id": 0})


def deposit_approve(vk_session, user_id, last_name, user_msg):
    deposit_user_id = Mongo.find_user(user_msg.split()[1])
    admin_id = user_id
    deposit = Mongo.check_deposit_amount(user_id)

    if deposit_user_id is None:
        msg = 'Комендант, ты че, у тебя такого бойца нет'
        vk_session.method('messages.send', {"user_id": admin_id, "message": msg, "random_id": 0})

    elif deposit is None:
        msg = 'Жеванный крот, лучше бы Чехов вел кассу...\nА если бы я не глянул?\n' \
              'От этого бойца переводов не поступало!!!'
        vk_session.method('messages.send', {"user_id": admin_id, "message": msg, "random_id": 0})

    else:
        Mongo.update_deposit_status(user_id, 1)
        row_num = [i.split()[0] for i in Sheet.boets_list()].index(last_name) + 1  # CHANGE TO +2 AFTER SWAP
        deposit_per_month = Sheet.cell_int_value(cell_id='G2')  # CHANGE AFTER SWAP
        leftover = Sheet.add_money(row_num, deposit, deposit_per_month)

        if leftover == 0:
            admin_msg = 'Шоколадно, пойду обрадую бойца. В табличке все поправил если че'
            user_msg = 'Боец - молодец, деньги пришли!'
        else:
            admin_msg = 'Либо я долблюсь в глаза, либо... у меня же нет глаз, тогда могу с уверенностью сказать,' \
                        'что это чудо в перьях перевело денег больше, чем нужно.\n Эх, филантропы'
            user_msg = 'Признавайся, ты наступил на поле "Благотворительность", играя в монополию?\n' \
                       'Ха-ха, расчехлил тебя! Если нет, то уведомляю, что я получил от тебя денег больше,' \
                       'чем нужно.\n Вот запись коменданта со скрытой камеры, когда он увидел это!\n' \
                       'https://www.youtube.com/watch?v=aEZndCsKthU'

        vk_session.method('messages.send', {"user_id": admin_id, "message": admin_msg, "random_id": 0})
        vk_session.method('messages.send', {"user_id": deposit_user_id['_id'], "message": user_msg, "random_id": 0})


def deposit_decline(vk_session, user_id, last_name, user_msg):
    admin_id = user_id

    if len(user_msg.split()) != 3:
        msg = 'Мастерок, что непонятного? Напиши "Не пришло (фамилия)"'
        vk_session.method('messages.send', {"user_id": admin_id, "message": msg, "random_id": 0})
        return 0

    deposit_user_id = Mongo.find_user(user_msg.split()[2].capitalize())

    if deposit_user_id is None:
        msg = 'Не гони на чела, он ведь даже не в отряде'
        vk_session.method('messages.send', {"user_id": admin_id, "message": msg, "random_id": 0})

    elif deposit is None:
        msg = 'Жеванный крот, лучше бы Чехов вел кассу...\nА если бы я не глянул?\n' \
              'От этого бойца переводов не поступало!!!'
        vk_session.method('messages.send', {"user_id": admin_id, "message": msg, "random_id": 0})

    else:
        Mongo.update_deposit_status(user_id, -1)

        msg = 'Ща я его быстренько отпетушарю'
        vk_session.method('messages.send', {"user_id": admin_id, "message": msg, "random_id": 0})

        msg = 'Слышь, где деньги Лебовски? За такое можно и в глаз!'
        vk_session.method('messages.send', {"user_id": deposit_user_id['_id'], "message": msg, "random_id": 0})


def call_cumendant(vk_session, user_id, last_name, user_msg):
    admin_id = Sheet.cell_int_value(cell_id='G1')  # CHANGE AFTER SWAP

    msg = f'Товарищ комендант, вас призывает {last_name}'
    vk_session.method('messages.send', {"user_id": admin_id, "message": msg, "random_id": 0})

    msg = 'Оно приближается...'
    vk_session.method('messages.send', {"user_id": user_id, "message": msg, "random_id": 0})
