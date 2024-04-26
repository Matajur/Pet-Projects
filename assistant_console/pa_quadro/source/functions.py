"""Module providing a functionality to manage the contacts in a contact list"""

from copy import deepcopy
from typing import Tuple

from .birthdays import search_upcoming_birthday_contacts
from .classes import Record, AddressBook, ValidationError, NoteBook, Notice
from .constants import (
    COLUMN_1,
    SEPARATOR,
    INDENT,
    FIELD,
    HEADER,
    SKIPPER,
    NOTE_HEADER,
    Color,
)
from .search_contacts import search_contacts_by_field
from .search_notes import search_notes_by_field


def input_error(message: str):
    """
    A decorator to add custom messages to the errors handling.

    :param message: an error message
    :return: a decorator for the errors handling
    """

    def decorator(func):
        """
        A decorator to handle input errors.

        :param func: function where an input error can occur
        :return: function if no input error occurred, or a description of the error
        """

        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValidationError:
                print(SEPARATOR)
                print(Color.RED + f"{INDENT}{message:<{FIELD}}|" + Color.RESET)
                print(SEPARATOR)
                return False
            except KeyError:
                print(SEPARATOR)
                print(Color.RED + f"{INDENT}{message:<{FIELD}}|" + Color.RESET)
                return False
            except ValueError:
                return "Invalid"

        return inner

    return decorator


def get_command(command: str):
    """
    A function to map user input to appropriate commands.

    :param command: user input in str format
    :return: function
    """
    commands = {
        "1": show_all,
        "2": contact_adder,
        "3": contact_manager,
        "4": search_contacts_by_field,
        "5": search_upcoming_birthday_contacts,
        "6": show_all,
        "7": note_adder,
        "8": note_manager,
        "9": search_notes_by_field,
        "help": helper,
    }

    cmd = commands.get(command)
    if not cmd:
        return invalid_command
    return cmd


def get_manager(command: str):
    """
    A function to map user input to appropriate commands.

    :param command: user input in str format
    :return: function
    """
    commands = {
        "1": name_setter,
        "2": address_setter,
        "3": address_resetter,
        "4": email_setter,
        "5": email_resetter,
        "6": phone_modifier,
        "7": phone_resetter,
        "8": birthday_setter,
        "9": birthday_resetter,
    }

    cmd = commands.get(command)
    if not cmd:
        return invalid_command
    return cmd


def contact_adder(book: AddressBook, *_) -> None:
    """
    Function to add new records to contact book

    :param book: a dictionary with user contacts
    :return: None, prints only a message about the success or failure of the operation
    """
    print(SEPARATOR)
    while True:
        record = Record()
        result = name_setter(record)
        if result == 1:
            print(SEPARATOR)
            print(SKIPPER)
            break
        if record.name.value in book.data.keys():
            print(SEPARATOR)
            print(
                Color.YELLOW
                + f"{INDENT}{f'Record with name {record.name.value} already exists':<{FIELD}}|"
                + Color.RESET
            )
            print(SEPARATOR)
        elif result == 2:
            break

    if record.name.value != "__default__":
        while True:
            if address_setter(record):
                break
        while True:
            if phone_setter(record):
                break
        if record.phones:
            print(
                Color.BLUE
                + f"{INDENT}{'Would you like to add one more phone or press Enter to skip'}: "
                + Color.RESET
            )
            while True:
                if phone_setter(record):
                    break
        while True:
            if email_setter(record):
                break
        while True:
            if birthday_setter(record):
                break

        if save_or_discard(record):
            book.add_record(record)
            print(SEPARATOR)
            print(
                Color.GREEN
                + f"{INDENT}{'New record added to address book':<{FIELD}}|"
                + Color.RESET
            )
        else:
            print(SEPARATOR)
            print(SKIPPER)


def note_adder(notebook: NoteBook, *_) -> None:
    """
    Function to add new notes to notebook

    :param notebook: a dictionary with user notes
    :return: None, prints only a message about the success or failure of the operation
    """
    print(SEPARATOR)
    notice = Notice()
    while True:
        result = note_setter(notice)
        if result == 1:
            print(SEPARATOR)
            print(SKIPPER)
            break
        if notice.note.value in notebook.data.keys():
            print(SEPARATOR)
            print(
                Color.YELLOW
                + f"{INDENT}{f'Record with name {notice.note.value} already exists':<{FIELD}}|"
                + Color.RESET
            )
            print(SEPARATOR)
        elif result == 2:
            break

    if notice.note.value != "__default__":
        for _ in range(3):
            if tag_setter(notice) == 1:
                break

        if save_or_discard(notice):
            notebook.add_notice(notice)
            print(SEPARATOR)
            print(
                Color.GREEN
                + f"{INDENT}{'New note added to notebook':<{FIELD}}|"
                + Color.RESET
            )
        else:
            print(SEPARATOR)
            print(SKIPPER)


@input_error("Exact this name is not present in the address book")
def contact_manager(book: AddressBook, *_) -> None:
    """
    Function to delete of update records

    :param book: a dictionary with user contacts
    :return: None, prints only a message about the success or failure of the operation
    """
    while True:
        record = contact_finder(book)
        if record is None:
            print(SEPARATOR)
            print(SKIPPER)
            return
        if record:
            break

    interface = {
        "1": "Modify contact name",
        "2": "Modify contact address",
        "3": "Delete contact address",
        "4": "Modify contact email",
        "5": "Delete contact email",
        "6": "Add or modify contact phone",
        "7": "Delete contact phone",
        "8": "Modify contact birthday",
        "9": "Modify contact birthday",
        "0": "Delete contact",
        "": "Enter to skip",
    }
    print(SEPARATOR)
    for key, value in interface.items():
        print(f"|{key:^{COLUMN_1}}|{value:<{FIELD}}|")
    print(SEPARATOR)

    while True:
        command = input(Color.BLUE + f"{INDENT}Type the command: " + Color.RESET)
        if command == "":
            print(SEPARATOR)
            print(SKIPPER)
            return
        if command == "0":
            record_eraser(record, book)
            return

        new_record = deepcopy(record)

        print(SEPARATOR)
        result = get_manager(command)(new_record)
        if result == 1:
            print(SEPARATOR)
            print(SKIPPER)
            break
        if result == 2:
            break

    if save_or_discard(new_record, record):
        book.delete(record.name.value)
        book.add_record(new_record)
        print(SEPARATOR)
        print(Color.GREEN + f"{INDENT}{'Contact updated':<{FIELD}}|" + Color.RESET)
    else:
        print(SEPARATOR)
        print(SKIPPER)


def address_resetter(record: Record) -> int:
    """
    Function to delete address

    :param record: a record from contact book
    :return: 2 if operation is successful
    """
    record.remove_address()
    return 2


def phone_resetter(record: Record) -> int:
    """
    Function to delete phone

    :param record: a record from contact book
    :return: 2 if operation is successful
    """
    for i, _ in enumerate(record.phones):
        print(f"|{i+1:^{COLUMN_1}}|{'Delete related number':<{FIELD}}|")

    print(f"{INDENT}{'Type Enter or any other button to skip':<{FIELD}}|")

    print(SEPARATOR)
    command = input(Color.BLUE + f"{INDENT}Type the command: " + Color.RESET)

    try:
        command = int(command) - 1
    except ValueError:
        pass
    if command not in list(range(len(record.phones))):
        return 1

    record.remove_phone(command)
    return 2


def birthday_resetter(record: Record) -> int:
    """
    Function to delete birthday

    :param record: a record from contact book
    :return: 2 if operation is successful
    """
    record.remove_birthday()
    return 2


def email_resetter(record: Record) -> int:
    """
    Function to delete email

    :param record: a record from contact book
    :return: 2 if operation is successful
    """
    record.remove_email()
    return 2


def record_eraser(record: Record | Notice, book: AddressBook | NoteBook) -> int:
    """
    Function to delete a record

    :param record: a dictionary with user contacts or notes
    :param book: a dictionary with user records
    :return: 3 if operation is successful
    """
    if isinstance(record, Record):
        book.delete(record.name.value)
    else:
        book.delete(record.note.value)
    print(SEPARATOR)
    print(Color.YELLOW + f"{INDENT}{'Record deleted':<{FIELD}}|" + Color.RESET)
    return 3


@input_error("Exact this note is not present in the note book")
def note_manager(notebook: NoteBook, *_) -> None:
    """
    Function to delete or update notes

    :param notebook: a dictionary with user notes
    :return: None, prints only a message about the success or failure of the operation
    """
    while True:
        record = note_finder(notebook)
        if record == 1:
            print(SEPARATOR)
            print(SKIPPER)
            return
        if isinstance(record, Notice):
            break

    interface = {
        "1": "Modify note",
        "2": "Add or modify tag",
        "3": "Delete tag",
        "0": "Delete note",
        "": "Enter to skip",
    }
    print(SEPARATOR)
    for key, value in interface.items():
        print(f"|{key:^{COLUMN_1}}|{value:<{FIELD}}|")
    print(SEPARATOR)

    while True:
        command = input(Color.BLUE + f"{INDENT}Type the command: " + Color.RESET)
        if command == "":
            print(SEPARATOR)
            print(SKIPPER)
            return
        if command == "0":
            record_eraser(record, notebook)  # type: ignore
            return

        new_record = deepcopy(record)

        print(SEPARATOR)
        result = get_handler(command)(new_record)
        if result == 1:
            print(SEPARATOR)
            print(SKIPPER)
            break
        if result == 2:
            break

    if save_or_discard(new_record, record):
        notebook.delete(record.note.value)
        notebook.add_notice(new_record)
        print(SEPARATOR)
        print(Color.GREEN + f"{INDENT}{'Note updated':<{FIELD}}|" + Color.RESET)
    else:
        print(SEPARATOR)
        print(SKIPPER)


def get_handler(command: str):
    """
    A function to map user input to appropriate commands.

    :param command: user input in str format
    :return: function
    """
    commands = {
        "1": note_setter,
        "2": tag_modifier,
        "3": tag_resetter,
    }

    cmd = commands.get(command)
    if not cmd:
        return invalid_command
    return cmd


def note_finder(notebook: NoteBook) -> Notice | int:
    """
    Function to find a note by key word

    :param notebook: a dictionary with user notes
    :return: note
    """
    print(SEPARATOR)
    hint = input(
        Color.BLUE
        + f"{INDENT}{'Enter a hint to search for a note to change or Enter to skip: '}"
        + Color.RESET
    ).lower()
    if hint == "":
        print(SEPARATOR)
        print(SKIPPER)
        return 1
    result = []
    for rec in notebook.data.values():
        if hint in rec.note.value.lower() or hint in rec.give_all_tags():
            result.append(rec)
    if not result:
        print(SEPARATOR)
        print(
            Color.YELLOW
            + f"{INDENT}{'No such word in your notes':<{FIELD}}|"
            + Color.YELLOW
        )
        return 2

    print(SEPARATOR)
    print(NOTE_HEADER)
    print(SEPARATOR)
    for number, record in enumerate(result):
        print(f"|{number + 1:^{COLUMN_1}}|{record}|")
    print(SEPARATOR)

    index = input(
        Color.BLUE
        + f"{INDENT}Type an index of the note you want to work with or Enter to skip: "
        + Color.RESET
    )
    try:
        index = int(index) - 1
    except ValueError:
        pass
    if index not in list(range(len(result))):
        return 1
    return result[index]


def tag_resetter(record: Notice) -> int:
    """
    Function to delete tag

    :param record: a record from contact book
    :return: 2 if operation is successful
    """
    for i, _ in enumerate(record.tags):
        print(f"|{i+1:^{COLUMN_1}}|{'Delete related number':<{FIELD}}|")

    print(f"{INDENT}{'Type Enter or any other button to skip':<{FIELD}}|")

    print(SEPARATOR)
    command = input(Color.BLUE + f"{INDENT}Type the command: " + Color.RESET)

    try:
        command = int(command) - 1
    except ValueError:
        pass
    if command not in list(range(len(record.tags))):
        return 1

    record.remove_tag(command)
    return 2


def tag_modifier(record: Notice) -> int:
    """
    Function to add or modify a tag in the record

    :param record: a record from note book
    :return: 2 if operation is successful or 1 if should be skipped
    """
    for i, _ in enumerate(record.tags):
        print(f"|{i+1:^{COLUMN_1}}|{'Modify related tag':<{FIELD}}|")
    if len(record.tags) != 3:
        print(f"|{9:^{COLUMN_1}}|{'Add new tag':<{FIELD}}|")

    print(f"{INDENT}{'Type Enter or any other button to skip':<{FIELD}}|")

    print(SEPARATOR)
    command = input(Color.BLUE + f"{INDENT}Type the command: " + Color.RESET)
    try:
        command = int(command) - 1
    except ValueError:
        pass
    if command == 8:
        while True:
            result = tag_setter(record)
            if result:
                return result
    if command not in list(range(len(record.tags))):
        return 1

    while True:
        result = tag_changer(record, command)
        if result:
            return result


def tag_changer(record: Notice, index: int) -> int:
    """
    Function to change a tag

    :param record: a record from the note book
    :param index: index of a tag to change
    :return: 2 if operation is successful or 1 if should be skipped
    """
    tag = input(
        Color.BLUE + f"{INDENT}{'Enter new tag or press Enter to skip'}: " + Color.RESET
    )
    if not tag:
        return 1
    record.modify_tag(tag, index)
    return 2


@input_error("Exact this name is not present in the address book")
def contact_finder(book: AddressBook) -> Record | None:
    """
    Function to find a contact by its name

    :param book: a dictionary with user contacts
    :return: record
    """
    print(SEPARATOR)
    name = input(
        Color.BLUE
        + f"{INDENT}{'Enter the exact name of the contact you want to change or Enter to skip'}: "
        + Color.RESET
    )
    if not name:
        return None
    return book.find(name.strip())


def save_or_discard(
    new_record: Record | Notice, *old_record: Record | Notice
) -> bool | None:
    """
    Function to save record o note

    :param old_record: a dictionary with user contacts or notes to be modified (optional)
    :param new_record: a dictionary with user contacts or notes that overwrights the original one
    :return: True if the record should be saved or None
    """
    print(SEPARATOR)
    if isinstance(new_record, Record):
        print(HEADER)
    else:
        print(NOTE_HEADER)
    print(SEPARATOR)
    if old_record:
        print(Color.YELLOW + f"|{'Old':^{COLUMN_1}}|{old_record[0]}|" + Color.RESET)
    print(Color.CYAN + f"|{'New':^{COLUMN_1}}|{new_record}|" + Color.RESET)
    print(SEPARATOR)
    print(Color.YELLOW + f"|{'0':^{COLUMN_1}}|{'Discard':<{FIELD}} " + Color.RESET)
    print(Color.CYAN + f"|{'1':^{COLUMN_1}}|{'Save':<{FIELD}} " + Color.RESET)
    print(SEPARATOR)
    decision = input(
        Color.BLUE + f"{INDENT}{'Would you like to save changes'}: " + Color.RESET
    )
    if decision == "1":
        return True


@input_error("The name must contain 3-20 characters")
def name_setter(record: Record) -> int:
    """
    Function to set record name

    :param book: a record from contact book
    :return: 2 if operation is successful or 1 if should be skipped
    """
    name = input(
        Color.BLUE
        + f"{INDENT}{'Enter new contact name or press Enter to skip and go back to main menu'}: "
        + Color.RESET
    )
    if not name:
        return 1
    record.add_name(name)
    return 2


def note_setter(notice: Notice) -> int:
    """
    Function to set notes

    :param notice: a record from note book
    :return: 2 if operation is successful or 1 if should be skipped
    """
    note = input(
        Color.BLUE
        + f"{INDENT}{'Enter new note or press Enter to skip and go back to main menu'}: "
        + Color.RESET
    )
    if not note:
        return 1
    notice.add_note(note)
    return 2


@input_error("The address must contain 3-40 characters")
def address_setter(record: Record) -> int:
    """
    Function to add address to a record

    :param record: a record from contact book
    :return: 2 if operation is successful or 1 if should be skipped
    """
    address = input(
        Color.BLUE
        + f"{INDENT}{'Enter new address or press Enter to skip'}: "
        + Color.RESET
    )
    if not address:
        return 1
    record.add_address(address)
    return 2


@input_error("The phone number must be in +380991234567 format")
def phone_setter(record: Record) -> int:
    """
    Function to add phone number to a record

    :param record: a record from contact book
    :return: 2 if operation is successful or 1 if should be skipped
    """
    phone = input(
        Color.BLUE
        + f"{INDENT}{'Enter new phone (ex. +380991234567) or press Enter to skip'}: "
        + Color.RESET
    )
    if not phone:
        return 1
    record.add_phone(phone)
    return 2


def phone_modifier(record: Record) -> int:
    """
    Function to add or modify a phone number in the record

    :param record: a record from contact book
    :return: 2 if operation is successful or 1 if should be skipped
    """
    for i, _ in enumerate(record.phones):
        print(f"|{i+1:^{COLUMN_1}}|{'Modify related number':<{FIELD}}|")
    if len(record.phones) != 2:
        print(f"|{9:^{COLUMN_1}}|{'Add new phone number':<{FIELD}}|")

    print(f"{INDENT}{'Type Enter or any other button to skip':<{FIELD}}|")

    print(SEPARATOR)
    command = input(Color.BLUE + f"{INDENT}Type the command: " + Color.RESET)
    try:
        command = int(command) - 1
    except ValueError:
        pass
    if command == 8:
        while True:
            result = phone_setter(record)
            if result:
                return result
    if command not in list(range(len(record.phones))):
        return 1

    while True:
        result = phone_changer(record, command)
        if result:
            return result


@input_error("The phone number must be in +380991234567 format")
def phone_changer(record: Record, index: int) -> int:
    """
    Function to change a phone

    :param record: a record from the address book
    :param index: index of a phone to change
    :return: 2 if operation is successful or 1 if should be skipped
    """
    phone = input(
        Color.BLUE
        + f"{INDENT}{'Enter new phone (ex. +380991234567) or press Enter to skip'}: "
        + Color.RESET
    )
    if not phone:
        return 1
    record.modify_phone(phone, index)
    return 2


def tag_setter(notice: Notice) -> int:
    """
    Function to add tags to a note

    :param notice: a record from note book
    :return: 2 if operation is successful or 1 if should be skipped
    """
    tag = input(
        Color.BLUE
        + f"{INDENT}{'Enter new tag or press Enter to finish operation'}: "
        + Color.RESET
    )
    if not tag:
        return 1
    notice.add_tag(tag)
    return 2


@input_error(
    "The birthday must be in DD.MM.YYYY format, not in future or more than 100 years ago"
)
def birthday_setter(record: Record) -> int:
    """
    Function to add birthday to a record

    :param record: a record from contact book
    :return: 2 if operation is successful or 1 if should be skipped
    """
    birthday = input(
        Color.BLUE
        + f"{INDENT}{'Enter new birthday (ex. DD.MM.YYYY) or press Enter to skip'}: "
        + Color.RESET
    )
    if not birthday:
        return 1
    record.add_birthday(birthday)
    return 2


@input_error("The email must be in example@mail.com format")
def email_setter(record: Record) -> int:
    """
    Function to add email to a record

    :param record: a record from contact book
    :return: 2 if operation is successful or 1 if should be skipped
    """

    email = input(
        Color.BLUE
        + f"{INDENT}{'Enter new email (ex. example@mail.com) or press Enter to skip'}: "
        + Color.RESET
    )
    if not email:
        return 1
    record.add_email(email)
    return 2


def invalid_command(*_) -> None:
    """
    Ivalid command handler.

    :return: None, only prints message about invalid command
    """
    print(SEPARATOR)
    print(Color.RED + f"{INDENT}{'Invalid command':<{FIELD}}|" + Color.RESET)


def show_all(book: AddressBook | NoteBook, *_) -> None:
    """
    Function of displaying a complete list of contacts or notes.

    :param book: a dictionary with user contacts or notes
    :return: None, only prints the contact list / notebook or a warning that the
            contact list / notebook is empty
    """
    chunk_size = 5
    sorted_book = dict(sorted(book.items()))
    items = list(sorted_book.values())
    total_items = len(items)
    if not total_items:
        print(SEPARATOR)
        print(
            Color.YELLOW
            + f"{INDENT}{'No records yet, please add':<{FIELD}}|"
            + Color.RESET
        )
        return

    print(SEPARATOR)
    if isinstance(book, AddressBook):
        print(HEADER)
    else:
        print(NOTE_HEADER)
    print(SEPARATOR)
    start_index = 0
    while start_index < total_items:
        end_index = min(start_index + chunk_size, total_items)
        current_chunk = items[start_index:end_index]

        for number, record in enumerate(current_chunk):
            print(f"|{number + 1 + start_index:^{COLUMN_1}}|{record}|")

        if end_index < total_items:
            input(Color.CYAN + f"{INDENT}Press Enter to continue: " + Color.RESET)

        start_index = end_index


@input_error("Invalid command")
def parse_input(user_input: str) -> Tuple[str, ...]:
    """
    Function to parse commands received from the user using the CLI.

    :param user: a string with a command and possible arguments
    :return cmd, *args: a tuple with a command in string format and
                        the arguments, if any, as a tuple of strings
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def helper(*_) -> None:
    """
    Function to provide hints for the user.
    """
    print(SEPARATOR)
    print(
        (
            Color.MAGENTA
            + f"{INDENT}{'Come on! No help needed, just select a command from the list below':<{FIELD}}|"
            + Color.RESET
        )
    )
