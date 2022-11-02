def wrong_cmd(vk_session, id):
    vk_session.method('messages.send', {"user_id": id, "message": "Я таких слов не знаю :(", "random_id": 0})

def help(vk_session, id):
    msg = "Список команд:жопажопа"
    vk_session.method('messages.send', {"user_id": id, "message": msg, "random_id": 0})
