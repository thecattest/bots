import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


try:
    from vk_token import TOKEN, GROUP_ID
except ImportError:
    print('Файл с логином и паролем не найден')
    exit(1)


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            from_id = event.object.message['from_id']
            user = vk.users.get(user_id=from_id, fields='city')[0]

            answer = f"Привет, {user['first_name']}!"
            if 'city' in user:
                answer += f"\nКак поживает {user['city']['title']}?"
            random_id = random.randint(0, 2 ** 64)

            vk.messages.send(user_id=from_id,
                             message=answer,
                             random_id=random_id)


if __name__ == '__main__':
    main()
