import vk_api
import os

try:
    from vk_token import LOGIN, PASSWORD, GROUP_ID, ALBUM_ID
except ImportError:
    print('Файл с логином и паролем не найден')
    exit(1)


def main():
    photo_path = 'static/img'
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    upload = vk_api.VkUpload(vk_session)

    photos = [os.path.join(photo_path, fn) for fn in os.listdir(photo_path)]
    upload.photo(photos, album_id=ALBUM_ID, group_id=GROUP_ID)


if __name__ == '__main__':
    main()
