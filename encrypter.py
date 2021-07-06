import base64


def encrypt(password):
    return base64.b64encode(bytes(password, encoding="utf-8"))

def decrypt(password):
    return base64.b64decode(bytes(password, encoding="utf-8"))
