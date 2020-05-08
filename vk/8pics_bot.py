import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


try:
    from vk_token import LOGIN, PASSWORD, TOKEN, GROUP_ID
except ImportError:
    print('Файл с логином и паролем не найден')
    exit(1)


def get_photos_ids(vk, owner_id):
    albums_info = [(album['id'], album['size']) for album in vk.photos.getAlbums(owner_id=owner_id)['items']]
    photos_ids = []
    for album_id, photos_count in albums_info:
        for i in range(photos_count // 1000 + 1):
            album_photos = vk.photos.get(owner_id=owner_id, album_id=album_id, offset=1000 * i, count=1000)['items']
            photos_ids.extend([(photo['id']) for photo in album_photos])
    return photos_ids


def get_random_url(owner_id, photos_ids):
    photo_id = random.choice(photos_ids)
    return f"photo{owner_id}_{photo_id}"


def main():
    OWNER_ID = -int(GROUP_ID)

    user_vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    try:
        user_vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    user_vk = user_vk_session.get_api()

    group_vk_session = vk_api.VkApi(
        token=TOKEN)
    group_vk = group_vk_session.get_api()
    longpoll = VkBotLongPoll(group_vk_session, GROUP_ID)

    photos_ids = get_photos_ids(user_vk, OWNER_ID)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object.message
            from_id = message['from_id']
            user = user_vk.users.get(user_id=from_id)[0]
            print(f"{user['first_name']} {user['last_name']}: {message['text']}")

            answer = f"Привет, {user['first_name']}!"
            photo = get_random_url(OWNER_ID, photos_ids)
            random_id = random.randint(0, 2 ** 64)
            group_vk.messages.send(user_id=from_id,
                                   message=answer,
                                   random_id=random_id,
                                   attachment=photo)


if __name__ == '__main__':
    main()
