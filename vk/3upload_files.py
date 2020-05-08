import vk_api
import os

try:
    from vk_token import LOGIN, PASSWORD
except ImportError:
    print('Файл с логином и паролем не найден')
    LOGIN = ''
    PASSWORD = ''


def main():
    album_id = 263568049
    group_id = 180439946
    photo_path = 'static/img'
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    upload = vk_api.VkUpload(vk_session)

    photos = [os.path.join(photo_path, fn) for fn in os.listdir(photo_path)]
    upload.photo(photos, album_id=album_id, group_id=group_id)


if __name__ == '__main__':
    main()
