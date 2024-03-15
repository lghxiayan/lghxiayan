from argon2 import PasswordHasher

def hash_password(password):
    """
    使用argon2库对密码进行哈希处理。

    :param password: 待哈希的密码字符串
    :return: 哈希后的密码
    """
    try:
        # 创建一个argon2.PasswordHasher实例
        hasher = PasswordHasher()
        # 使用哈希器对密码进行哈希处理
        hashed_password = hasher.hash(password)
        return hashed_password
    except Exception as e:
        # 处理可能发生的异常
        raise RuntimeError(f"密码哈希过程中发生错误: {e}")

# 测试密码
password = "QQ316122141"
# 调用函数进行密码哈希
hashed_password = hash_password(password)

print("原始密码:", password)
print("哈希密码:", hashed_password)
