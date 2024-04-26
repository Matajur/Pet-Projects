"""Module providing a console bot assistant with CLI"""

import pickle

from .source.classes import AddressBook, NoteBook
from .source.constants import COLUMN_1, SPAN, FIELD, INDENT, SEPARATOR, Color
from .source.functions import get_command, parse_input

BACKUP = "backup.dat"
STORAGE = "storage.dat"


def loader() -> tuple[AddressBook, NoteBook]:
    """
    Function to load saved contact book.

    :return: contact book
    """
    book = AddressBook()
    try:
        with open(BACKUP, "rb") as file:
            book.data = pickle.load(file)
    except FileNotFoundError:
        pass

    notebook = NoteBook()
    try:
        with open(STORAGE, "rb") as file:
            notebook.data = pickle.load(file)
    except FileNotFoundError:
        pass
    return (book, notebook)


def main() -> None:
    """
    Function that provides Command Line Interface.
    """
    print(SEPARATOR)
    print(Color.GREEN + f"|{'Welcome to the assistant bot!':^{SPAN}}|" + Color.RESET)
    book, notebook = loader()
    if book.data:
        print(
            Color.GREEN
            + f"|{'Contact book successfully loaded':^{SPAN}}|"
            + Color.RESET
        )

    while True:
        plotter()
        print(SEPARATOR)
        user_input = input(Color.BLUE + f"{INDENT}Type the command: " + Color.RESET)
        command, *args = parse_input(user_input)

        if command == "exit":
            print(SEPARATOR)
            decision = (
                input(
                    Color.BLUE
                    + f"{INDENT}Do you want to save changes? Y/N [Y]: "
                    + Color.RESET
                )
                .lower()
                .strip()
            )
            print(SEPARATOR)
            if decision in ("y", ""):
                saver(book, notebook)
                print(
                    Color.GREEN
                    + f"{INDENT}{'Changes saved, good bye!':<{FIELD}}|"
                    + Color.RESET
                )
                print(SEPARATOR)
                break
            print(Color.GREEN + f"{INDENT}{'Good bye!':<{FIELD}}|" + Color.RESET)
            print(SEPARATOR)
            break

        if command in ("6", "7", "8", "9"):
            get_command(command)(notebook, *args)
        else:
            get_command(command)(book, *args)


def plotter() -> None:
    """
    Main interface of the console bot
    """
    interface = {
        "1": "Show all records from contact book",
        "2": "Add new contact",
        "3": "Manage contact",
        "4": "Find contact",
        "5": "Upcoming birthdays",
        "6": "Show all records from notebook",
        "7": "Add new note",
        "8": "Manage note",
        "9": "Find note",
        "help": "Help hints",
        "exit": "Exit the bot",
    }
    print(SEPARATOR)
    for key, value in interface.items():
        print(f"|{key:^{COLUMN_1}}|{value:<{FIELD}}|")


def saver(book: AddressBook, notebook: NoteBook) -> None:
    """
    Function to save contact book to file.

    :param book: contact book
    """
    if book.data:
        with open(BACKUP, "wb") as file:
            pickle.dump(book.data, file)
    if notebook.data:
        with open(STORAGE, "wb") as file:
            pickle.dump(notebook.data, file)


if __name__ == "__main__":
    main()
