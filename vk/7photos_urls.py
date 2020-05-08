import vk_api
from pprint import pprint


try:
    from vk_token import LOGIN, PASSWORD, GROUP_ID, USER_ID
except ImportError:
    print('Файл с логином и паролем не найден')
    exit(1)


def main():
    OWNER_ID = -int(GROUP_ID)
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()

    albums_info = [(album['id'], album['size']) for album in vk.photos.getAlbums(owner_id=OWNER_ID)['items']]
    photos_urls = []
    for album_id, photos_count in albums_info:
        for i in range(photos_count // 1000 + 1):
            album_photos = vk.photos.get(owner_id=OWNER_ID, album_id=album_id, offset=1000*i, count=1000)['items']
            photos_urls.extend([(photo['sizes'][-1]) for photo in album_photos])
    print(*photos_urls, sep='\n')


if __name__ == '__main__':
    main()
