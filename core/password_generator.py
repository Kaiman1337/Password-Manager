# password_generator.py
import random
import string
from core.error_codes import ERROR_CODES, PASSWORD_GENERATOR_PREFIX

UPPER = string.ascii_uppercase
LOWER = string.ascii_lowercase
NUMBERS = string.digits
SYMBOLS = '~`!@#$%^&*()_-+={[}]|\\:;"\'<,>.?/'

def gen_pass(length, use_symbols, use_numbers):
    char_pool = list(UPPER + LOWER)
    if use_symbols:
        char_pool += list(SYMBOLS)
    if use_numbers:
        char_pool += list(NUMBERS)

    password = ''.join(random.choice(char_pool) for _ in range(length))
    return password
