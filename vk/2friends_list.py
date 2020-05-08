import vk_api

try:
    from vk_token import LOGIN, PASSWORD
except ImportError:
    print('Файл с логином и паролем не найден')
    exit(1)


def main():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()

    response = vk.friends.get(order='name', fields='bdate')
    for friend in sorted(response['items'], key=lambda x: x['last_name']):
        name = f"{friend['last_name']} {friend['first_name']}"
        bday = friend['bdate'] if 'bdate' in friend else 'Дата рождения не указана'
        print(f"{name}: {bday}")


if __name__ == '__main__':
    main()