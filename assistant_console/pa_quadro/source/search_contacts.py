"""Module providing a functionality to search contacts in a contact list"""

import re
from typing import Callable, Any

from .classes import AddressBook
from .constants import COLUMN_1, SEPARATOR, FIELD, INDENT, HEADER, Color


def search_contacts_by_field(book: AddressBook, *_) -> None:
    """
    The method for searching contacts.

    :param book: An AddressBook
    :return: None
    """

    if len(book) == 0:
        print(SEPARATOR)
        print(
            Color.YELLOW + f"{INDENT}{'Contact book is empty':<{FIELD}}|" + Color.RESET
        )
        return

    handler = get_search_by_method()
    if not handler:
        return

    contacts = dict(sorted(book.items()))
    result = handler(contacts)
    show_result(result)


def get_search_by_method() -> Callable[[Any], Any]:
    """
    The method allows you to select the field to be searched in and returns the desired function.

    :return: Callable
    """

    print(SEPARATOR)
    print(f"|{'1':^{COLUMN_1}}|{'Find contact by name':<{FIELD}}|")
    print(f"|{'2':^{COLUMN_1}}|{'Find contact by phone':<{FIELD}}|")
    print(f"|{'3':^{COLUMN_1}}|{'Find contact by birthday':<{FIELD}}|")
    print(f"|{'4':^{COLUMN_1}}|{'Find contact by e-mail':<{FIELD}}|")
    print(f"|{'5':^{COLUMN_1}}|{'Find contact by address':<{FIELD}}|")
    print(f"{INDENT}{'Other to exit':<{FIELD}}|")
    print(SEPARATOR)
    command = input(Color.BLUE + f"{INDENT}{'Type the command'}: " + Color.RESET)
    commands = {
        "1": search_contacts_by_name,
        "2": search_contacts_by_phone,
        "3": search_contacts_by_birthday,
        "4": search_contacts_by_email,
        "5": search_contacts_by_address,
    }
    return commands.get(command)  # type: ignore


def search_contacts_by_name(contacts: AddressBook) -> list:
    """
    The method for searching contacts by name.

    :param contacts: The contacts
    :return: The list of contacts
    """

    while True:
        print(SEPARATOR)
        input_value = input(Color.BLUE + f"{INDENT}{'Enter name'}: " + Color.RESET)
        if 2 < len(input_value) < 21:
            result = []
            for _, record in enumerate(contacts.values()):
                search_by_name = record.search_by_name(input_value)
                if search_by_name:
                    result.append(search_by_name)
            return result

        print(SEPARATOR)
        print(
            Color.RED
            + f"{INDENT}{'The name must contain 3-20 characters':<{FIELD}}|"
            + Color.RESET
        )


def search_contacts_by_phone(contacts: AddressBook) -> list:
    """
    The method for searching contacts by phone.

    :param contacts: The contacts
    :return: The list of contacts
    """

    while True:
        print(SEPARATOR)
        input_value = input(
            Color.BLUE + f"{INDENT}{'Enter phone (ex. +380991234567)'}: " + Color.RESET
        )
        if re.match(r"^\+?\d+$", input_value):
            result = []
            for _, record in enumerate(contacts.values()):
                search_by_phone = record.search_by_phone(input_value)
                if search_by_phone:
                    result.append(search_by_phone)
            return result

        print(SEPARATOR)
        print(
            Color.RED
            + f"{INDENT}{'The phone number must have +380991234567 format':<{FIELD}}|"
            + Color.RESET
        )


def search_contacts_by_birthday(contacts: AddressBook) -> list:
    """
    The method for searching contacts by birthday.

    :param contacts: The contacts
    :return: The list of contacts
    """

    while True:
        print(SEPARATOR)
        input_value = input(
            Color.BLUE + f"{INDENT}{'Enter birthday (ex. DD.MM.YYYY)'}: " + Color.RESET
        )
        if re.match(r"^[\d.]+$", input_value):
            result = []
            for _, record in enumerate(contacts.values()):
                search_by_birthday = record.search_by_birthday(input_value)
                if search_by_birthday:
                    result.append(search_by_birthday)
            return result

        print(SEPARATOR)
        print(
            Color.RED
            + f"{INDENT}{'Birthday must be in DD.MM.YYYY format':<{FIELD}}|"
            + Color.RESET
        )


def search_contacts_by_email(contacts: AddressBook) -> list:
    """
    The method for searching contacts by email.

    :param contacts: The contacts
    :return: The list of contacts
    """

    while True:
        print(SEPARATOR)
        input_value = input(
            Color.BLUE
            + f"{INDENT}{'Enter email (ex. example@mail.com)'}: "
            + Color.RESET
        )
        if 2 < len(input_value) < 41:
            result = []
            for _, record in enumerate(contacts.values()):
                search_by_email = record.search_by_email(input_value)
                if search_by_email:
                    result.append(search_by_email)
            return result

        print(SEPARATOR)
        print(
            Color.RED
            + f"{INDENT}{'The email must be in example@mail.com format':<{FIELD}}|"
            + Color.RESET
        )


def search_contacts_by_address(contacts: AddressBook) -> list:
    """
    The method for searching contacts by address.

    :param contacts: The contacts
    :return: The list of contacts
    """

    while True:
        print(SEPARATOR)
        input_value = input(
            Color.BLUE
            + f"{INDENT}{'Enter address or press Enter to skip'}: "
            + Color.RESET
        )
        if 2 < len(input_value) < 41:
            result = []
            for _, record in enumerate(contacts.values()):
                search_by_address = record.search_by_address(input_value)
                if search_by_address:
                    result.append(search_by_address)
            return result

        print(SEPARATOR)
        print(
            Color.RED
            + f"{INDENT}{'The address must contain 3-40 characters':<{FIELD}}|"
            + Color.RESET
        )


def show_result(result: list) -> None:
    """
    The method to display the result.

    :param result: The list of contacts
    :return: None
    """

    if len(result):
        print(SEPARATOR)
        print(HEADER)
        print(SEPARATOR)
        for number, record in enumerate(result):
            print(f"|{number + 1:^{COLUMN_1}}|{record}|")
    else:
        print(SEPARATOR)
        print(f"|{' ' * COLUMN_1}|{'Empty result':<{FIELD}}|")
