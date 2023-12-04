from difflib import SequenceMatcher
from mods.log_config import get_logger_error
from mods.logic import (
    ab_printer,
    bot,
    contact_adder,
    contact_search,
    contact_selector,
    days_to_birthdays,
    exit_func,
    hello_user,
    loader,
    saver,
    show_all_contacts,
)
from mods.sorter import sort_files


logger = get_logger_error(__name__)


def helper():
    result = "List of all supported commands:\n\n"
    for key in commands:
        result += "{:<13} {:<50}\n".format(key, commands[key][1])
    return result


def unknown_command(phrase: str) -> str:
    if len(phrase) < 4:
        return f'Unknown command "{phrase}"\n'
    else:
        result = ""
        subcomands = phrase.split(" ")
        for key, value in commands.items():
            for el in subcomands:
                if len(el) > 2 and el in key:
                    if key not in result:
                        result += f"{key}{value[1]}\n"

            if len(key) >= len(phrase):
                start = 0
                end = len(phrase) - 1
                while True:
                    if (
                        SequenceMatcher(a=phrase, b=key[start:end]).ratio() > 0.6
                        and key not in result
                    ):
                        result += f"{key}{value[1]}\n"
                    start += 1
                    end += 1
                    if end > len(key) - 1:
                        break

        if result:
            return f'Unknown command "{phrase}"\nDid you mean:\n{result}'
        else:
            return f'Unknown command "{phrase}"\n'


commands = {
    "hello": (hello_user, " -> just greating"),
    "exit": (exit_func, " -> exit from the bot with or without saving"),
    "close": (exit_func, " -> exit from the bot with or without saving"),
    "save": (saver, " -> saves to file all changes"),
    "load": (loader, " -> loads last version of the Address Book"),
    "help": (helper, " -> shows the list of all supported commands"),
    "create": (contact_adder, " -> adds new contact"),
    "+c": (contact_adder, " -> adds new contact (short command)"),
    "show all": (show_all_contacts, " -> shows all contacts"),
    "?c": (show_all_contacts, " -> shows all contacts (short command)"),
    "search": (contact_search, " -> search for a contact by name"),
    "?s": (contact_search, " -> search for a contact by name (short command)"),
    "modify": (contact_selector, " -> removes or modifies an existing contact"),
    "-c": (
        contact_selector,
        " -> remove or modify an existing contact (short command)",
    ),
    "to birthdays": (days_to_birthdays, " -> days to birthgays"),
    "?b": (days_to_birthdays, " -> days to birthgays (short command)"),
    "print all": (ab_printer, " -> printing complete address book"),
    "pa": (ab_printer, " -> printing complete address book (short command)"),
    "sort": (sort_files, " -> sort files by category in a selected folder"),
    "so": (
        sort_files,
        " -> sort files by category in a selected folder (short command)",
    ),
}


def main():
    bot.greating()
    print(loader())
    while True:
        phrase = input('Please enter command or type "help": ').strip()

        result = bot.command_handler(phrase, commands)
        print(result)
        if result == "":
            unknown_command(phrase)
        elif result == "Goodbye!\n":
            break


if __name__ == "__main__":
    main()
