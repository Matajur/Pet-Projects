import pickle
from datetime import datetime
from mods.fields import Address, Birthday, Email, Name, Note, Phone, Record
from mods.handler import Bot
from mods.log_config import get_logger_error


bot = Bot()

logger = get_logger_error(__name__)


def ab_printer() -> str:
    print("Printing all records:\n")
    return bot.book


# What exactly to do with address
def address_handler(record: Record):
    choice = input(
        "Select a number to proceed: 0 - Remove Address, 1 - Replace Address, or press Enter to skip: "
    )
    if choice == "0":
        record.set_address(None)
        print(f'\nAddress of the contact "{record.name}" has been removed\n')
    elif choice == "1":
        return address_setter(record)
    else:
        print("\nOperation skipped\n")


def address_setter(record: Record) -> None:
    address = Address(input("Enter address or press Enter to skip: "))
    if address.validator() != False:
        record.set_address(address)
        print(f'\nAddress "{address}" set\n')
    else:
        print("\nOperation skipped\n")


# What exactly to do with birthday
def birthday_handler(record: Record):
    choice = input(
        "Select a number to proceed: 0 - Remove Birthday, 1 - Replace Birthday, or press Enter to skip: "
    )
    if choice == "0":
        record.set_birthday(None)
        print(f'\nBirthday of the contact "{record.name}" has been removed\n')
    elif choice == "1":
        return birthday_setter(record)
    else:
        print("\nOperation skipped\n")


def birthday_setter(record: Record) -> None:
    while True:
        birthday = Birthday(
            input("Enter birthday (ex. 2023-12-25) or press Enter to skip: ")
        )
        if birthday.validator() == True:
            record.set_birthday(birthday)
            print(f'\nBirthday "{birthday}" set\n')
            break
        elif birthday.validator() == False:
            print("\nOperation skipped\n")
            break
        else:
            print(f'Wrong date "{birthday}" format')


# Creating a new contact with all its fields
def contact_adder() -> str:
    record = Record("__blank")
    if name_setter(record) == "Stop":
        return "New contact not created\n"

    address_setter(record)
    phone_setter(record)
    email_setter(record)
    birthday_setter(record)
    note_setter(record)

    bot.book.add_record(record)
    return f"\nAdded contact\n{record}"


# What exactly to do with contact
def contact_eraser(key: str) -> str:
    choice = input(
        "Select a number to proceed: 0 - Remove Contact, or press Enter to skip: "
    )
    if choice == "0":
        bot.book.erase_record(key)
        return f'\nContact "{key}" has been removed\n'
    else:
        return "\nOperation skipped\n"


# Selecting what exactly to be modified for a contact
def contact_mod_selector(key: str, record: Record):
    while True:
        choice = input(
            "Select a number to proceed: 0-Contact, 1-Name, 2-Adress, 3-Phones, 4-Email, 5-Birthday, 6-Notes, or press Enter to skip: "
        )
        if choice == "":
            return "\nOperation skipped\n"
        elif choice == "0":
            return contact_eraser(key)
        elif choice == "1":
            result = name_handler(record)
            if result != "Stop":
                bot.book.records[result.value] = bot.book.records[key]
                bot.book.erase_record(key)
        elif choice == "2":
            address_handler(record)
        elif choice == "3":
            phone_handler(record)
        elif choice == "4":
            email_handler(record)
        elif choice == "5":
            birthday_handler(record)
        elif choice == "6":
            note_handler(record)
        else:
            print(f'\nUnsupported selection "{choice}"\n')
        print(f'Do you want to continue working with this contact"?')


def contact_search() -> str:
    inquiry = input("Enter search query: ").lower()

    result = []
    for record in bot.book.records.values():
        if inquiry in record.__getitem__().lower():
            result.append(record)

    if result:
        contacts_info = "\n".join(str(record) for record in result)
        return f"\nContacts found:\n\n{contacts_info}"

    return f'No contacts found for "{inquiry}"'


# Searching a contact to be modified
def contact_selector():
    name = input("Enter the exact contact name: ")
    for key, record in bot.book.records.items():
        if key == name:
            print(f"\nContact found:\n{record}")
            return contact_mod_selector(key, record)
    return f'Contact "{name}" not found'


def days_to_birthdays() -> str:
    days = int(input("Enter the number of days: "))
    today = datetime.today().date()
    result = ""

    for record in bot.book.records.values():
        if record.birthday is not None:
            dob = record.birthday.birthday
            dob_this_year = dob.replace(year=today.year)

            if dob_this_year < today:
                dob_this_year = dob_this_year.replace(year=today.year + 1)

            days_to_birthday = (dob_this_year - today).days
            if days_to_birthday <= days:
                result += f"\n{record}"
    if result == "":
        return "\nNo contacts with upcoming birthdays\n"
    else:
        return f"\nContacts with upcoming birthdays in the next {days} days:\n{result}"


# What exactly to do with email
def email_handler(record: Record):
    choice = input(
        "Select a number to proceed: 0 - Remove Email, 1 - Replace Email, or press Enter to skip: "
    )
    if choice == "0":
        record.set_email(None)
        print(f'\nEmail of the contact "{record.name}" has been removed\n')
    elif choice == "1":
        return email_setter(record)
    else:
        print("\nOperation skipped\n")


def email_setter(record: Record) -> None:
    while True:
        email = Email(
            input("Enter email (ex. abc@gmail.com) or press Enter to skip: "))
        if email.validator() == True:
            record.set_email(email)
            print(f'\nEmail "{email}" set\n')
            break
        elif email.validator() == False:
            print("\nOperation skipped\n")
            break
        else:
            print(f'Wrong email "{email}" format')


def exit_func() -> str:
    a = input("Would you like to save changes (Y/N)? ")
    if a == "Y" or a == "y":
        print(saver())
    return "Goodbye!\n"


def hello_user() -> str:
    return "\nHow can I help you?\n"


def loader() -> str:
    try:
        with open("backup.dat", "rb") as file:
            global bot
            bot.book = pickle.load(file)
        return "\nAddress Book successfully loaded from backup.dat\n"
    except:
        logger.error("No file")
        return "No contact information saved"


# What exactly to do with name
def name_handler(record: Record):
    choice = input(
        "Select a number to proceed: 1 - Replace Name, or press Enter to skip: "
    )
    if choice == "1":
        return name_setter(record)
    else:
        print("\nOperation skipped\n")


def name_setter(record: Record) -> str:
    name = Name(input("Enter contact name (cannot be empty): "))
    while True:
        if name.value in bot.book.records.keys():
            name = Name(
                input(
                    f'Contact "{name}" already exists, enter new name o press Enter to exit: '
                )
            )
            if name.validator() == False:
                print("\nOperation skipped\n")
                return "Stop"
        else:
            if name.validator() != False:
                record.set_name(name)
                print(f'\nName "{name}" set\n')
                return name
            else:
                name = Name(
                    input(
                        "Contact name cannot be empty, enter contact name o press Enter to exit: "
                    )
                )
                if name.validator() == False:
                    print("\nOperation skipped\n")
                    return "Stop"


def note_eraser(record: Record) -> None:
    temp = record.show_listed_items(record.notes)
    if temp is None:
        print(f'"{record.name}" has no notes assigned\n')
    else:
        print(temp)
        index = int(
            input(
                "Enter a position number of the note to remove (0 to remove all), or any other button to skip: "
            )
        )
        if index == 0:
            record.set_note(None)
            print(f"{record.name} has no more notes assigned\n")
        elif 1 <= index <= len(record.notes):
            note = record.notes[index - 1]
            record.erase_listed_items(record.notes, index)
            print(
                f'\nNote "{note}" has been removed from contact {record.name}\n')
        else:
            print("\nOperation skipped\n")


# What exactly to do with notes
def note_handler(record: Record):
    choice = input(
        "Select a number to proceed: 0 - Remove All or Selected Note, 1 - Replace Selected Note, 2 - Add New Note, or press Enter to skip: "
    )
    if choice == "0":
        return note_eraser(record)
    elif choice == "1":
        return note_modifier(record)
    elif choice == "2":
        return note_setter(record)
    else:
        print("\nOperation skipped\n")


def note_modifier(record: Record) -> None:
    temp = record.show_listed_items(record.notes)
    if temp is None:
        print(f'"{record.name}" has no notes assigned\n')
    else:
        print(temp)
        index = int(
            input(
                "Enter a position number of the note to replace, or press Enter to skip: "
            )
        )
        if 1 <= index <= len(record.notes):
            note = record.notes[index - 1]
            new_note = note_setter(record, False)
            record.modify_listed_item(record.notes, index, new_note)
            print(
                f'\nPhone number "{note}" has been replaced with "{new_note}"\n')
        else:
            print("\nOperation skipped\n")


def note_setter(record: Record, new=True) -> Note:
    while True:
        note = Note(input("Enter new note o press Enter to skip: "))
        if note.validator() != False and new == True:
            record.set_note(note)
            print(f'\nNote "{note}" set\n')
        elif note.validator() != False and new == False:
            return note
        else:
            print("\nOperation skipped\n")
            break


def phone_eraser(record: Record) -> None:
    temp = record.show_listed_items(record.phones)
    if temp is None:
        print(f'"{record.name}" has no phones assigned\n')
    else:
        print(temp)
        index = int(
            input(
                "Enter a position number of the phone to remove (0 to remove all), or press Enter to skip: "
            )
        )
        if index == 0:
            record.set_phone(None)
            print(f"\n{record.name} has no more phones assigned\n")
        elif 1 <= index <= len(record.phones):
            phone = record.phones[index - 1]
            record.erase_listed_items(record.phones, index)
            print(
                f'\nPhone number "{phone}" has been removed from contact {record.name}\n'
            )
        else:
            print("\nOperation skipped\n")


# What exactly to do with phone
def phone_handler(record: Record):
    choice = input(
        "Select a number to proceed: 0 - Remove All or Selected Phone, 1 - Replace Selected Phone, 2 - Add New Phone, or press Enter to skip: "
    )
    if choice == "0":
        return phone_eraser(record)
    elif choice == "1":
        return phone_modifier(record)
    elif choice == "2":
        return phone_setter(record)
    else:
        print("\nOperation skipped\n")


def phone_modifier(record: Record) -> None:
    temp = record.show_listed_items(record.phones)
    if temp is None:
        print(f'"{record.name}" has no phones assigned\n')
    else:
        print(temp)
        index = int(
            input(
                "Enter a position number of the phone to replace, or press Enter to skip: "
            )
        )
        if 1 <= index <= len(record.phones):
            phone = record.phones[index - 1]
            new_phone = phone_setter(record, False)
            record.modify_listed_item(record.phones, index, new_phone)
            print(
                f'\nPhone number "{phone}" has been replaced with "{new_phone}"\n')
        else:
            print("\nOperation skipped\n")


def phone_setter(record: Record, new=True):
    while True:
        count = 0
        phone = Phone(
            input("Enter new phone (ex. +38(099)1234567) or press Enter to skip: ")
        )

        if phone.validator() == False:
            print("\nOperation skipped\n")
            break

        for ph in record.phones:
            if ph.value == phone.value:
                print(
                    f'Contact "{record.name}" has already this "{phone}" number')
                count += 1

        if count == 0:
            if phone.validator() == True and new == True:
                record.set_phone(phone)
                print(f'\nPhone "{phone}" set\n')
            elif phone.validator() == True and new == False:
                return phone
            else:
                print(f'Wrong phone "{phone}" format')


def saver() -> str:
    if bot.book.records:
        with open("backup.dat", "wb") as file:
            pickle.dump(bot.book, file)
        return "\nAddress Book successfully saved to backup.dat\n"
    else:
        return "\nAddress Book is empty, no data to be saved to file\n"


def show_all_contacts() -> str:
    if bot.book.records:
        N = int(input("How many contacts to show? "))
        if N < 1:
            return "\nInput cannot be less that 1\n"
        elif N >= len(bot.book.records):
            result = "\nPrintting all records:\n"
            for key, value in bot.book.records.items():
                result += f"\n{value}"
            result += "\nEnd of address book\n"
            return result
        else:
            iter = bot.book.iterator(N, bot.book.records)
            for i in iter:
                print(i)
                input("Press any key to continue:\n")
            if len(bot.book.records) % 2 == 0:
                return "\nEnd of address book\n"
            else:
                return (
                    f"{str(list(bot.book.records.values())[-1])}\nEnd of address book\n"
                )
    else:
        return "No contacts, please add\n"


if __name__ == "__main__":
    ab_printer()
