import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime


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
            message = event.object.message
            from_id = message['from_id']
            user = vk.users.get(user_id=from_id, fields='city')[0]
            print(f"{user['first_name']} {user['last_name']}: {message['text']}")

            try:
                date = datetime.datetime.strptime(message['text'], '%Y-%m-%d')
                answer = date.strftime('%A')
            except ValueError:
                answer = "Отправь мне дату в формате YYYY-MM-DD и я скажу тебе день недели"

            random_id = random.randint(0, 2 ** 64)
            vk.messages.send(user_id=from_id,
                             message=answer,
                             random_id=random_id)


if __name__ == '__main__':
    main()
