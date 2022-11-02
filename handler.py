from mongo import Mongo

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
    vk_session.method('messages.send', {"user_id": id, "message": "Я таких слов не знаю :(", "random_id": 0})

def help(vk_session, id):
    msg = "Список команд:жопажопа"
    vk_session.method('messages.send', {"user_id": id, "message": msg, "random_id": 0})
