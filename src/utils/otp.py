
from random import choice
import string


def random_otp(digits: int):
    chars = string.digits
    return "".join(choice(chars) for _ in range(digits))
