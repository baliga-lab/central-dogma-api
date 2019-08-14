import os
from base64 import b64encode
from argon2 import PasswordHasher

# requires argon2-cffi

SALT_SIZE = 32
def make_password(passwd):
    ph = PasswordHasher()
    salt = b64encode(os.urandom(SALT_SIZE)).decode('utf-8')
    s = passwd + salt
    hashval = ph.hash(s)
    return salt, hashval


def verify_password(password, salt, hashv):
    try:
        ph = PasswordHasher()
        return ph.verify(hashv, password + salt)
    except:
        return False
