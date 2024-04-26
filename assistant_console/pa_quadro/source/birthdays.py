"""Module providing a function to display a list of colleagues with upcoming birthdays"""

from datetime import datetime, timedelta, date

from .classes import AddressBook
from .constants import COLUMN_1, SEPARATOR, INDENT, HEADER, FIELD


def search_upcoming_birthday_contacts(book: AddressBook, *_) -> None:
    """
    The method checks whether there are contacts in the list.

    :return: None
    """

    if len(book) == 0:
        print(SEPARATOR)
        print(f"|{' ' * COLUMN_1}|{'Contact book is empty':<{FIELD}}|")
        return

    handle_book(book)


def handle_book(book: AddressBook) -> None:
    """
    The method displays information on found contacts.

    :return: None
    """

    days = get_days()
    today = datetime.now().date()
    end_date = today + timedelta(days=days)
    contacts = get_contacts(book, today, end_date)

    print(SEPARATOR)
    print(
        f"{INDENT}{'Days range ' + today.strftime('%d.%m.%Y') + ' - ' + end_date.strftime('%d.%m.%Y'):<{FIELD}}|"
    )

    if len(contacts) > 0:
        print(SEPARATOR)
        print(HEADER)
        print(SEPARATOR)
        for number, record in enumerate(contacts):
            print(f"|{number + 1:^{COLUMN_1}}|{record}|")
    else:
        print(SEPARATOR)
        print(
            f"|{' ' * COLUMN_1}|{'There are no happy birthday contacts in this range':<{FIELD}}|"
        )


def get_days() -> int:
    """
    The method returns the number of days entered by the user.

    :return: integer
    """

    while True:
        print(SEPARATOR)
        input_value = input(
            f"{INDENT}{'Enter the number of days for which birthdays will be displayed starting from today'}: "
        )
        if input_value and input_value.isdigit():
            return int(input_value)

        print(SEPARATOR)
        print(f"{INDENT}{'The number must be of integer type only':<{FIELD}}|")


def get_contacts(book: AddressBook, today: date, end_date: date) -> list:
    """
    The method filters contacts falling within a date range by the birthday field.

    :return: list
    """

    contacts = []
    for contact in book.values():
        if contact.birthday is not None:
            formatted = datetime(
                year=today.year, month=contact.birthday.month, day=contact.birthday.day
            ).date()
            if today <= formatted <= end_date:
                contacts.append(contact)
    return contacts
