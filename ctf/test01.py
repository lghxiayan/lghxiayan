from cryptography.fernet import Fernet


def encrypt(key, plain_text):
    f = Fernet(key)
    return f.encrypt(plain_text)


def decrypt(key, cipher):
    f = Fernet(key)
    return f.decrypt(cipher)


if __name__ == "__main__":
    key = Fernet.generate_key()
    print(f"key={key}")

    # cipher_text = encrypt(key=key, plain_text=b"attack")
    # print(cipher_text)

    cipher_text = b'U2FsdGVkX18BkpB/W9lD7ZGSP5BprjbrL/WKn+7fn8gWCXpmDW+y/5FoVYPd5pIFCZfHFiov'
    plain_text = decrypt(key=key, cipher=cipher_text)
    print(plain_text)
