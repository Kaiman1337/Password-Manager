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
 
    password_chars = []

    # First character: prefer uppercase if allowed, else lowercase, else any
    if use_big_letters:
        first_char = random.choice(UPPER)
    elif use_small_letters:
        first_char = random.choice(LOWER)
    else:
        first_char = random.choice(char_pool)

    password_chars.append(first_char)

    # Fill the rest of the password
    while len(password_chars) < length:
        r = random.random()

        if use_symbols and r < 0.2:  # 20% chance to pick symbol
            symbol_choice = custom_symbols if custom_symbols else SYMBOLS
            password_chars.append(random.choice(symbol_choice))
        elif use_numbers and r < 0.35:  # additional 35% chance to pick number
            password_chars.append(random.choice(NUMBERS))
        else:
            password_chars.append(random.choice(UPPER + LOWER if use_big_letters and use_small_letters else
                                               UPPER if use_big_letters else
                                               LOWER if use_small_letters else
                                               char_pool))

    return ''.join(password_chars)