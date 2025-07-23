# error_codes.py
PASSWORD_GENERATOR_PREFIX = "[PASSWORD GENERATOR]:"

RED = "\033[91m"
RESET = "\033[0m"

ERROR_CODES = {
    "ERR_INVALID_PASS_LENGTH": f"{RED}[INVALID LENGTH]{RESET} Please enter a number between 8 and 256.",
    "ERR_INVALID_PASS_PREFERENCES_INPUT": f"{RED}[INVALID INPUT]{RESET} Please answer \"Yes\" or \"No.\"",
    "ERR_EMPTY_POOL": f"{RED}[EMPTY POOL]{RESET} No characters available to generate password.",
}
