import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import handler
from secret import TOKEN

vk_session = vk_api.VkApi(token=TOKEN)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

cmds = {
    "помощь": handler.help
}

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            print(session_api.users.get(user_ids=(id))[0])
            if msg not in cmds:
                handler.wrong_cmd(vk_session, id)
            for name, func in cmds.items():
                if msg.lower() == name:
                    func(vk_session, id)
                    break
