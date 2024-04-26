"""Module providing the classes to manage the contacts in a contact book"""

import re
from collections import UserDict
from datetime import datetime

from .constants import COLUMN_2, COLUMN_3, COLUMN_4, COLUMN_5, COLUMN_6


class ValidationError(Exception):
    """
    Error of creating an entry with an inappropriate field format.
    """


class Field:
    """
    A base class for record fields.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Address(Field):
    """
    A class for storing an address. Has length validation from 3 to 40 characters.
    """

    @property
    def value(self):
        """
        A method that validates name.
        """

        return self._value

    @value.setter
    def value(self, name):
        """
        A method that validates name.
        """

        if not 2 < len(str(name)) < 41:
            raise ValidationError()
        self._value = name


class Birthday(Field):
    """
    A class for storing a birthday. Has format validation (DD.MM.YYYY).
    """

    @property
    def value(self):
        """
        A method that validates name.
        """

        return self._value

    @property
    def month(self):
        """
        A method that validates month.
        """

        return self._value.month

    @property
    def day(self):
        """
        A method that validates day.
        """

        return self._value.day

    @value.setter
    def value(self, birthday):
        """
        A method that validates name.
        """

        try:
            birth = datetime.strptime(birthday, "%d.%m.%Y").date()
        except ValueError as exc:
            raise ValidationError() from exc
        if not 0 <= (datetime.today().date() - birth).days <= 100 * 365.4:
            raise ValidationError()
        self._value = datetime.strptime(birthday, "%d.%m.%Y").date()

    def __str__(self):
        return str(self.value.strftime("%d.%m.%Y"))


class Email(Field):
    """
    A class for storing a birthday. Has format validation (example@email.com).
    """

    @property
    def value(self):
        """
        A method that validates name.
        """

        return self._value

    @value.setter
    def value(self, email):
        """
        A method that validates name.
        """
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise ValidationError()
        self._value = email


class Name(Field):
    """
    A class for storing a contact name. Required field, min 3, max 20 characters.
    """

    @property
    def value(self):
        """
        A method that validates name.
        """

        return self._value

    @value.setter
    def value(self, name):
        """
        A method that validates name.
        """

        if not 2 < len(str(name)) < 21:
            raise ValidationError()
        self._value = name


class Note(Field):
    """
    A class for storing notes.
    """


class Phone(Field):
    """
    A class for storing a phone number. Has format validation (10 digits).
    """

    @property
    def value(self):
        """
        A method that validates phone number.
        """

        return self._value

    @value.setter
    def value(self, phone):
        """
        A method that validates phone number.
        """

        if not re.match(r"\+\d{12}", phone):
            raise ValidationError()
        self._value = phone


class Tag(Field):
    """
    A class of tags for notes.
    """


class Record:
    """
    A class for storing information about a contact, including name and contacts list.
    """

    def __init__(self):
        self.name = Name("__default__")
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_address(self, address: str):
        """
        A method that adds an address to the record.
        """

        self.address = Address(address)

    def add_birthday(self, birthday: str):
        """
        A method that adds a birthday to the record.
        """

        self.birthday = Birthday(birthday)

    def add_email(self, email: str):
        """
        A metod that adds an email to the record.
        """

        self.email = Email(email)

    def add_name(self, name: str):
        """
        A method that adds a name to the record.
        """

        self.name = Name(name)

    def add_phone(self, phone: str):
        """
        A method that adds a new phone number to the record.
        """

        self.phones.append(Phone(phone))

    def remove_address(self):
        """
        A method that removes the address from the record.
        """
        self.address = None

    def remove_birthday(self):
        """
        A method that removes the birthday from the record.
        """
        self.birthday = None

    def remove_email(self):
        """
        A method that removes the email from the record.
        """
        self.email = None

    def remove_phone(self, index: int):
        """
        A method that removes a phone number from the record.
        """

        self.phones.pop(index)

    def modify_phone(self, phone: str, index: int):
        """
        A method that modifies a phone in the record.
        """
        self.phones[index] = Phone(phone)

    def edit_phone(self, phones: list):
        """
        A method that edits a phone number in the record.
        """

        index = self.find_phone(phones[0])
        self.phones[index] = Phone(phones[1])

    def find_phone(self, phone: str):
        """
        A method that finds an index of the phone number in the record.
        """

        index = 0
        for item in self.phones:
            if item.value == phone:
                return index
            index += 1
        raise ValidationError()

    def search_by_name(self, name: str):
        """
        The method checks if the name matches the passed value.
        """

        if name.lower() in self.name.value.lower():
            return self

    def search_by_phone(self, phone: str):
        """
        The method checks if the phone matches the passed value.
        """

        for item in self.phones:
            if phone in item.value:
                return self

    def search_by_birthday(self, birthday: str):
        """
        The method checks if the birthday matches the passed value.
        """

        if birthday in str(self.birthday):
            return self

    def search_by_email(self, email: str):
        """
        The method checks if the email matches the passed value.
        """

        if email.lower() in str(self.email).lower():
            return self

    def search_by_address(self, address: str):
        """
        The method checks if the address matches the passed value.
        """

        if address.lower() in str(self.address).lower():
            return self

    def __str__(self) -> str:
        numbers = (
            "; ".join(f"{i + 1}: {p.value}" for i, p in enumerate(self.phones))
            if self.phones
            else None
        )
        return f"{self.name.value:^{COLUMN_2}}|{str(self.email):^{COLUMN_3}}|{str(numbers):^{COLUMN_4}}|{str(self.birthday):^{COLUMN_5}}|{str(self.address):^{COLUMN_6}}"


class Notice:
    """
    A class for storing user notes.
    """

    def __init__(self):
        self.note = Name("__default__")
        self.tags = []

    def add_note(self, note: str):
        """
        A method that adds a note to notice.
        """

        self.note = Note(note)

    def add_tag(self, tag: str):
        """
        A method that adds a new tag to the notice.
        """

        self.tags.append(Tag(tag))

    def remove_tag(self, index: int):
        """
        A method that removes a tag from the notice.
        """

        self.tags.pop(index)

    def edit_tag(self, tags: list):
        """
        A method that edits a tag in the notice.
        """

        index = self.find_tag(tags[0])
        self.tags[index] = Tag(tags[1])

    def find_tag(self, tag: str):
        """
        A method that finds an index of the tag in the notice.
        """

        index = 0
        for item in self.tags:
            if item.value == tag:
                return index
            index += 1
        raise ValidationError()

    def search_by_note(self, note: str):
        """
        The method checks if the note matches the passed value.
        """

        if note.lower() in str(self.note).lower():
            return self

    def search_by_tag(self, tag: str):
        """
        The method checks if the tag matches the passed value.
        """

        for item in self.tags:
            if tag.lower() in str(item).lower():
                return self

    def give_all_tags(self) -> list:
        """
        The method return all the notes as list of strings.
        """
        result = [i.value.lower() for i in self.tags]
        return result

    def modify_tag(self, tag: str, index: int):
        """
        A method that modifies a tag in the record.
        """
        self.tags[index] = Tag(tag)

    def __str__(self) -> str:
        numbers = (
            "; ".join(f"{i + 1}: {p.value}" for i, p in enumerate(self.tags))
            if self.tags
            else None
        )
        return f"{str(numbers):^{COLUMN_2 + COLUMN_3 + 1}}|{self.note.value:^{COLUMN_4 + COLUMN_5 + COLUMN_6 + 2}}"


class AddressBook(UserDict):
    """
    A class for storing and managing records.
    """

    def add_record(self, record: Record) -> None:
        """
        A method that adds a record to the address book.
        """

        if str(record.name) in self.data.keys():
            raise ValidationError()
        self.data[str(record.name)] = record

    def find(self, name: str) -> Record:
        """
        A method that finds a record in the address book.
        """

        return self.data[name]

    def delete(self, name: str) -> None:
        """
        A method that removes a record from the address book.
        """

        self.data.pop(name)


class NoteBook(UserDict):
    """
    A class for storing and managing notes with tags.
    """

    def add_notice(self, notice: Notice) -> None:
        """
        A method that adds a notice to the note book.
        """

        if str(notice.note) in self.data.keys():
            raise ValidationError()
        self.data[str(notice.note)] = notice

    def find(self, note: str) -> Notice:
        """
        A method that finds a notice in the note book.
        """

        return self.data[note]

    def delete(self, note: str) -> None:
        """
        A method that removes a record from the address book.
        """

        self.data.pop(note)
