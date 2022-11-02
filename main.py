import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import handler
from secret import TOKEN

vk_session = vk_api.VkApi(token=TOKEN)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

cmds = {
    "помощь": handler.help_user,
    "бабло": handler.payment_amount,
    "чек": handler.notification,
    "внес": handler.deposit
}

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            user_id = event.user_id
            last_name = session_api.users.get(user_ids=user_id)[0]['last_name']
            # Checking if user is registered in our system
            handler.is_registered(user_id, last_name)

            msg = event.text.lower()

            if msg not in cmds:
                handler.wrong_cmd(vk_session, user_id)
            else:
                for name, func in cmds.items():
                    if msg.lower() == name:
                        func(vk_session, user_id, last_name)
                        break
