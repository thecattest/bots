import vk_api
import datetime

try:
    from vk_token import LOGIN, PASSWORD
except ImportError:
    print('Файл с логином и паролем не найден')
    LOGIN = ''
    PASSWORD = ''


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()

    response = vk.wall.get(count=5, filter='owner')
    if response['items']:
        for note in response['items']:
            timestamp = note['date']
            text = note['text']
            date_obj = datetime.datetime.fromtimestamp(timestamp)
            date = date_obj.strftime('date: {%Y-%m-%d}, time: {%H:%M:%S}')
            print(f"{{'{text}'}};\n{date}\n")


if __name__ == '__main__':
    main()