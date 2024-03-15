import base64

encoded_string = "u2fsdgvkx1/lhjqfmn5njua/dinvzvwwnxcuxvulu6nuvzzuzvz5aazk7t2udkwsrnxckjnclqcqusylbyuh1j20o7iukdog=="
decoded_bytes = base64.b64decode(encoded_string)
decoded_string = decoded_bytes.decode('utf-8')

print(decoded_string)
