from abc import ABC, abstractclassmethod
from collections import UserDict
from copy import deepcopy
from mods.fields import Record, Field


class AddressBook(UserDict):
    def __init__(self, record: Record | None = None) -> None:
        self.records = {}
        if record is not None:
            self.add_record(record)

    def add_record(self, record: Record) -> None:
        self.records[record.name.value] = record

    def erase_record(self, key: str) -> None:
        del self.records[key]

    def iterator(self, quantity_to_show: int, listed_items: list[Field]) -> str:
        counter = 0
        result = f"\nPrinting {quantity_to_show} contacts"
        for item, record in listed_items.items():
            result += f"\n{str(record)}"
            counter += 1
            if counter >= quantity_to_show:
                yield result
                counter = 0
                result = f"\nPrinting next {quantity_to_show} contacts"

    def __str__(self) -> str:
        return "\n".join(
            f"Key:      {name}\n{record}" for name, record in self.records.items()
        )

    def __deepcopy__(self, memodict={}):
        copy_ab = AddressBook(self, self.records)
        memodict[id(self)] = copy_ab
        for el in self.records:
            copy_ab.append(deepcopy(el, memodict))
        return copy_ab


class Handler(ABC):
    @abstractclassmethod
    def command_handler(self) -> str:
        pass


class Bot(Handler):
    def __init__(self):
        self.book = AddressBook()

    def command_handler(self, phrase: str, commands: dict):
        command = None
        for key in commands:
            if phrase.lower() == key:
                command = key
                break
        if command is None:
            result = ""
        else:
            handler = commands.get(command)[0]
            result = handler()
        return result

    def greating(self):
        print("\nHello, I'm your you personal assistant! Are you ready to rock?")
