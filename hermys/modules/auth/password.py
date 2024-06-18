import re

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

SPECIAL_CHARACTERS = ['!', '@', '#', '$', '%', '*', '.', '+', '-']
ph = PasswordHasher()


def get_hashed_password(password: str):
    return ph.hash(password)


def verify_password(password: str, hashed_password: str):
    try:
        return ph.verify(hashed_password, password)
    except VerifyMismatchError:
        return False


def is_password_strong(password: str):
    if len(password) < 8:
        raise ValueError('Password should be at least 8')

    if not re.search('[0-9]', password):
        raise ValueError('Password must have at least one digit')

    if not re.search('[a-z]', password):
        raise ValueError('Password must have at least one lowercase letter')

    if not re.search('[A-Z]', password):
        raise ValueError('Password must have at least one uppercase letter')

    if not re.search(
        f'[{re.escape("".join(SPECIAL_CHARACTERS))}]',
        password,
    ):
        raise ValueError(
            'Password must have at least one especial character '
            f'({", ".join(SPECIAL_CHARACTERS)})'
        )

    return password
