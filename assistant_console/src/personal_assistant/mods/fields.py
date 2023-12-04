import re
from abc import ABC, abstractclassmethod
from datetime import datetime
from mods.log_config import get_logger_error


logger = get_logger_error(__name__)


class Field(ABC):
    @abstractclassmethod
    def __str__(self) -> str:
        pass

    @abstractclassmethod
    def validator(self) -> bool:
        pass


class Address(Field):
    def __init__(self, address: str) -> None:
        self.value = address

    def __str__(self) -> str:
        return self.value

    def validator(self) -> bool:
        if self.value == "":
            return False


class Birthday(Field):
    def __init__(self, birthday: str) -> None:
        self.value = birthday

    def __str__(self) -> str:
        return str(self.value)

    def validator(self) -> bool:
        if self.value == "":
            return False
        try:
            formatted_birthday = datetime.strptime(
                self.value, "%Y-%m-%d").date()
            if 100 * 365 > (datetime.today().date() - formatted_birthday).days > 0:
                self.value = formatted_birthday
                return True
        except:
            logger.error("Wrong date format")


class Email(Field):
    def __init__(self, email: str) -> None:
        self.value = email

    def __str__(self) -> str:
        return self.value

    def validator(self) -> bool:
        if self.value == "":
            return False
        if re.fullmatch(r"[a-zA-Z]{1}[\w\.]+@[a-zA-Z]+\.[a-zA-Z]{2,3}", self.value):
            return True


class Name(Field):
    def __init__(self, name: str) -> None:
        self.value = name

    def __str__(self) -> str:
        return self.value

    def validator(self) -> bool:
        if self.value == "":
            return False


class Note(Field):
    def __init__(self, note: str) -> None:
        self.value = note

    def __str__(self) -> str:
        return self.value

    def validator(self) -> bool:
        if self.value == "":
            return False


class Phone(Field):
    def __init__(self, phone: str) -> None:
        self.value = phone

    def __str__(self) -> str:
        return self.value

    def validator(self) -> bool:
        if self.value == "":
            return False
        elif re.fullmatch(r"\+[\d]{2}\([\d]{3}\)[\d]{7}", self.value):
            return True


class Record:
    def __init__(
        self,
        name: Name,
        address: Address = None,
        phone: list[Phone] = None,
        email: Email = None,
        birthday: Birthday = None,
        note: list[Note] = None,
    ):
        self.name = name
        self.address = address
        self.phones = []
        self.email = email
        self.birthday = birthday
        self.notes = []

    def set_name(self, name: Name):
        self.name = name

    def set_address(self, address: Address | None):
        self.address = address

    def set_email(self, value: Email | None):
        self.email = value

    def set_birthday(self, value: Birthday | None):
        self.birthday = value

    def set_phone(self, phone: Phone | None):
        if phone == None:
            self.phones.clear()
        else:
            self.phones.append(phone)

    def set_note(self, note: Note | None):
        if note == None:
            self.phones.clear()
        else:
            self.notes.append(note)

    def erase_listed_items(self, listed_item: list[Field], index: int):
        del listed_item[index - 1]

    def modify_listed_item(self, listed_item: list[Field], index: int, value: str):
        listed_item[index - 1] = value

    def show_listed_items(self, listed_item: list[Field]) -> str:
        if listed_item:
            result = ""
            for inx, p in enumerate(listed_item):
                result += f"{inx+1}: {p}  "
        else:
            result = None
        return result

    def __str__(self) -> str:
        return f"Name:     {self.name}\nAddress:  {self.address}\nPhones:   {self.show_listed_items(self.phones)}\nEmail:    {self.email}\nBirthday: {self.birthday}\nNotes:    {self.show_listed_items(self.notes)}\n"

    def __getitem__(self) -> str:
        return f"{self.name} {self.address} {self.show_listed_items(self.phones)} {self.email} {self.birthday} {self.show_listed_items(self.notes)}"
