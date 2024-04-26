"""Module providing a functionality to search notes in a notebook list"""

from typing import Callable, Any

from .classes import NoteBook
from .constants import COLUMN_1, SEPARATOR, FIELD, INDENT, NOTE_HEADER, Color


def search_notes_by_field(notebook: NoteBook, *_) -> None:
    """
    The method for searching notes.

    :param notebook: An NoteBook
    :return: None
    """

    if len(notebook) == 0:
        print(SEPARATOR)
        print(Color.YELLOW + f"{INDENT}{'Note book is empty':<{FIELD}}|" + Color.RESET)
        return

    search_method = get_search_method()
    if not search_method:
        return

    notes_all = dict(sorted(notebook.items()))
    notes_filtered = search_method(notes_all)
    show_result(notes_filtered)


def get_search_method() -> Callable[[Any], Any]:
    """
    The method allows you to select the field to be searched in and returns the desired function.

    :return: Callable
    """

    print(SEPARATOR)
    print(f"|{'1':^{COLUMN_1}}|{'Find notes by tag':<{FIELD}}|")
    print(f"|{'2':^{COLUMN_1}}|{'Find notes by text':<{FIELD}}|")
    print(f"{INDENT}{'Other to exit':<{FIELD}}|")
    print(SEPARATOR)

    command = input(Color.BLUE + f"{INDENT}{'Type the command'}: " + Color.RESET)
    commands = {
        "1": search_by_tag,
        "2": search_by_text,
    }
    return commands.get(command)  # type: ignore


def search_by_tag(notebook: NoteBook) -> list:
    """
    The method for searching notes by tags.

    :param notebook: The notebook
    :return: The list of notes
    """

    while True:
        print(SEPARATOR)

        input_value = input(Color.BLUE + f"{INDENT}{'Enter tag'}: " + Color.RESET)
        if 1 < len(input_value) < 21:
            result = []
            for _, notice in enumerate(notebook.values()):
                notice_with_tag = notice.search_by_tag(input_value)
                if notice_with_tag:
                    result.append(notice_with_tag)
            return result

        print(SEPARATOR)
        print(
            Color.RED
            + f"{INDENT}{'The tag must contain 2-20 characters':<{FIELD}}|"
            + Color.RESET
        )


def search_by_text(notebook: NoteBook) -> list:
    """
    The method for searching notes by text.

    :param notebook: The notebook
    :return: The list of notes
    """

    while True:
        print(SEPARATOR)

        input_value = input(Color.BLUE + f"{INDENT}{'Enter text'}: " + Color.RESET)
        if 1 < len(input_value) < 41:
            result = []
            for _, notice in enumerate(notebook.values()):
                notice_with_text = notice.search_by_note(input_value)
                if notice_with_text:
                    result.append(notice_with_text)
            return result

        print(SEPARATOR)
        print(
            Color.RED
            + f"{INDENT}{'The text must contain 2-40 characters':<{FIELD}}|"
            + Color.RESET
        )


def show_result(result: list) -> None:
    """
    The method to display the result.

    :param result: The list of notes
    :return: None
    """

    if len(result):
        print(SEPARATOR)
        print(NOTE_HEADER)
        print(SEPARATOR)
        for number, notice in enumerate(result):
            print(f"|{number + 1:^{COLUMN_1}}|{notice}|")
    else:
        print(SEPARATOR)
        print(f"|{' ' * COLUMN_1}|{'Empty result':<{FIELD}}|")
