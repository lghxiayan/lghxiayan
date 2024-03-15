import json


def get_stored_username():
    """如果存储了用记名，就获取它"""
    filename = 'username.json'
    try:
        with open(filename) as f:
            username = json.load(f)
    except FileNotFoundError:
        return None
    else:
        return username


def get_new_username():
    """提示用户输入用户名"""
    filename = 'username.json'
    username = input('你叫什么名字：')
    with open(filename, 'w') as f:
        json.dump(username, f)
    return username


def greet_user():
    """问候用户，并指出其名字"""
    username = get_stored_username()
    if username:
        print(f"Welcome back, {username}")
    else:
        username = get_new_username()
        print(f"We will remember you when you come back, {username}")


greet_user()
