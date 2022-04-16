import secrets
import string


def gen_str_slug(n: int) -> str:
    alphabet = string.ascii_letters
    return "".join(secrets.choice(alphabet) for _ in range(n))


def gen_int_slug(n: int) -> str:
    alphabet = string.digits
    return "".join(secrets.choice(alphabet) for _ in range(n))
