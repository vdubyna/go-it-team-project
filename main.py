import pickle
from fields.address_book import AddressBook
from fields.record import Record

from decorators import input_error


@input_error
def parse_input(user_input: str) -> tuple:
    """Parse user input into command and arguments."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args: list, book: AddressBook) -> str:
    """Add a new contact to the address book."""
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list, book: AddressBook) -> str:
    """Update an existing contact in the address book."""
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        return f"The record with name '{name}' is not found."

    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args: list, book: AddressBook) -> str:
    """Show the phone number for the contact."""
    name = args[0]
    record = book.find(name)
    if record is None:
        return f"The record with name '{name}' is not found."

    return str(record)


def show_all_contacts(book: AddressBook) -> str:
    """Show all contacts."""
    if not book:
        return "Contacts are empty."

    return "\n".join(f"{name}: {phone}" for name, phone in book.data.items())


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return f"The record with name '{name}' is not found."

    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)

    if record is None:
        return f"The record with name '{name}' is not found."

    if record.birthday is None:
        return f"No birthday for {name}"

    return f"{name}'s birthday is {record.birthday}"


@input_error
def birthdays(args, book: AddressBook):
    return book.get_upcoming_birthdays()


def save_data(book: AddressBook, filename: str = "var/addressbook.pkl") -> None:
    """Save data to a file using pickle serialization."""

    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename: str = "var/addressbook.pkl") -> AddressBook:
    """Load data from a file using pickle deserialization."""

    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()


def main() -> None:
    """Main function to handle user input and commands."""

    print("Welcome to the assistant bot!")
    address_book_file = "var/addressbook.pkl"
    contacts = load_data(address_book_file)

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in {"close", "exit"}:
            save_data(contacts, address_book_file)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all_contacts(contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(args, contacts))
        else:
            print("Invalid command.")
        print()


if __name__ == "__main__":
    main()
