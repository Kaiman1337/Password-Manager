# password_generator.py
import random
import string
from core.error_codes import ERROR_CODES, PASSWORD_GENERATOR_PREFIX

UPPER = string.ascii_uppercase
LOWER = string.ascii_lowercase
NUMBERS = string.digits
SYMBOLS = '~`!@#$%^&*()_-+={[}]|\\:;"\'<,>.?/'

def gen_pass(length, use_symbols, use_numbers, custom_symbols=None, use_big_letters=True, use_small_letters=True):
    char_pool = []

    if use_symbols:
        symbols_to_use = custom_symbols if custom_symbols is not None else SYMBOLS
        char_pool += list(symbols_to_use)

    if use_numbers:
        char_pool += list(NUMBERS)

    if use_big_letters:
        char_pool += list(UPPER)
    
    if use_small_letters:
        char_pool += list(LOWER)

    if not char_pool:
        return ""

    return ''.join(random.choice(char_pool) for _ in range(length))

