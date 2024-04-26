"""Module providing the constants"""


class Color:
    """
    A class providing colors for console outputs.
    """

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"


COLUMN_1 = 6
COLUMN_2 = 20
COLUMN_3 = 25
COLUMN_4 = 35
COLUMN_5 = 12
COLUMN_6 = 40
SPAN = COLUMN_1 + COLUMN_2 + COLUMN_3 + COLUMN_4 + COLUMN_5 + COLUMN_6 + 5
FIELD = SPAN - COLUMN_1 - 1
INDENT = f"|{' ' * COLUMN_1}|"
HEADER = f"|{'#':^{COLUMN_1}}|{'FULLNAME':^{COLUMN_2}}|{'EMAIL':^{COLUMN_3}}|{'PHONES':^{COLUMN_4}}|{'BIRTHDAY':^{COLUMN_5}}|{'ADDRESS':^{COLUMN_6}}|"
NOTE_HEADER = f"|{'#':^{COLUMN_1}}|{'TAGS':^{COLUMN_2 + COLUMN_3 + 1}}|{'NOTE':^{COLUMN_4 + COLUMN_5 + COLUMN_6 + 2}}|"
SKIPPER = Color.YELLOW + f"{INDENT}{'Operation skipped':<{FIELD}}|" + Color.RESET
SEPARATOR = "-" * (SPAN + 2)
