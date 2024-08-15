import pickle
from fields.address_book import AddressBook
from fields.record import Record
from InquirerPy import inquirer
from colorama import init, Fore
from fields.validators import validate_name, validate_phone, validate_email, validate_address, validate_birthday
from fields.notes import Note, Notes
from decorators import input_error
from tabulate import tabulate
from utils.suggest_input import suggest_name_input
from utils import parse_input, parse_flags

init(autoreset=True)



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
def show_phone(args: list, book: AddressBook) -> str:
    """Show the phone number for the contact."""
    name = args[0]
    record = book.find(name)
    if record is None:
        return f"The record with name '{name}' is not found."

    return str(record)


@input_error
def delete_contact(args, book: AddressBook):
    if len(args) != 1:
        return "Invalid number of arguments. Usage: delete-contact [name]"

    name = args[0]
    record = book.find(name)
    if record:
        book.delete(name)
        return f"Contact '{name}' successfully deleted"

    return f"No contact with the name '{name}' exists"


def show_all_contacts(book: AddressBook) -> str:
    """Show all contacts in a formatted table."""
    if not book:
        return "Contacts are empty."

    table = []
    for record in book.data.values():
        phones = "; ".join(phone.value for phone in record.phones)
        email = record.email.value if record.email else "N/A"
        address = record.address.value if record.address else "N/A"
        birthday = record.birthday.date.strftime("%d.%m.%Y") if record.birthday else "N/A"

        table.append([record.name.value, phones, email, address, birthday])

    return tabulate(table, headers=["Name", "Phone", "Email", "Address", "Birthday"], tablefmt="grid")
    # flags, skipped = parse_flags(args, ['tag', 'sort', 'order'])
    # tag = flags.get('tag', '')
    # sort = flags.get('sort', 'name')
    # order = flags.get('order', 'asc')
    # records = book.get_records(sort, order, tag)
    # if skipped:
    #     print('Unknown arguments:', skipped)
    # return "\n".join(f"{record.name}: {record}" for record in records)


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


@input_error
def add_tags(args, book: AddressBook):
    name, *tags = args
    record = book.find(name)
    if record is None:
        return f"The record with name '{name}' is not found."

    record.add_tags(tags)
    return "Tags added."


@input_error
def remove_tags(args, book: AddressBook):
    name, *tags = args
    record = book.find(name)
    if record is None:
        return f"The record with name '{name}' is not found."

    record.remove_tags(tags)
    return "Tags removed."


@input_error
def add_note(notes: Notes, title: str) -> str:
    """Add a new note to notes."""
    if notes.find_note(title):
        return f"Note with title '{title}' already exists."

    text = input("Enter a text: ")
    try:
        message = notes.add_note(title, text)
        return message
    except ValueError as e:
        return str(e)


@input_error
def change_note(notes: Notes, title: str) -> str:
    """Change the existing note by its title."""
    if not (note := notes.find_note(title)):
        return f"Note with title: '{title}' is not found."

    new_content = input("Enter new content: ")
    if new_content:
        note.content = new_content

    return f"Note with title '{title}' successfully edited."


@input_error
def delete_note(notes: Notes, title: str) -> str:
    """Delete the existing note by its title."""
    if not notes.find_note(title):
        return f"Note with title: '{title}' is not found."

    message = notes.delete_note(title)
    return message


@input_error
def find_note(notes: Notes, title: str) -> str | Note:
    """Find the existing note by its title."""
    if not (note := notes.find_note(title)):
        return f"Note with title: '{title}' is not found."

    return note


@input_error
def show_all_notes(notes: Notes) -> str:
    """Show all existing notes."""
    return notes.show_all()


def save_data(book: AddressBook, notes: Notes, filename: str = "var/addressbook.pkl") -> None:
    """Save data to a file using pickle serialization."""

    with open(filename, "wb") as file:
        data = {"address_book": book, "notes": notes}
        pickle.dump(data, file)


def load_data(filename: str = "var/addressbook.pkl") -> (AddressBook, Notes):
    """Load data from a file using pickle deserialization."""

    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)
            return data.get("address_book", AddressBook()), data.get("notes", Notes())
    except FileNotFoundError:
        return AddressBook(), Notes()


@input_error
def search_contacts(query: str, book: AddressBook) -> str:
    """Search for contacts by any field."""
    results = []
    query_lower = query.lower()

    for record in book.data.values():
        found = False

        # Check name
        if query_lower in str(record.name).lower():
            results.append(str(record))
            found = True

        # Check phones
        if not found:
            for phone in record.phones:
                if query_lower in phone.value:
                    results.append(str(record))
                    found = True
                    break

        # Check email
        if not found and record.email and query_lower in str(record.email.value):
            results.append(str(record))
            found = True

        # Check address
        if not found and record.address and query_lower in str(record.address.value):
            results.append(str(record))
            found = True

        # Check birthday
        if not found and record.birthday and query_lower in str(record.birthday.value):
            results.append(str(record))
            found = True

    if results:
        return "\n".join(results)
    return "No matching contacts found."


@input_error
def add_contact_interactive(book: AddressBook) -> str:
    """Interactively add a new contact to the address book."""

    # Input name with validation
    while True:
        name = input(Fore.LIGHTYELLOW_EX + "Name: " + Fore.RESET)
        if validate_name(name):
            break
        print(Fore.LIGHTRED_EX + "Invalid name. Please use only letters.")

    # Input phone with validation
    while True:
        phone = input(Fore.LIGHTYELLOW_EX + "Phone: " + Fore.RESET)
        if validate_phone(phone):
            break
        print(Fore.LIGHTRED_EX + "Invalid phone number. Please enter a valid number (at least 10 digits).")

    # Input email with validation
    while True:
        email = input(Fore.LIGHTYELLOW_EX + "Email: " + Fore.RESET)
        if not email or validate_email(email):
            break
        print(Fore.LIGHTRED_EX + "Invalid email address. Please enter a valid email.")

    # Input address with validation
    while True:
        address = input(Fore.LIGHTYELLOW_EX + "Address: " + Fore.RESET)
        if not address or validate_address(address):
            break
        print(Fore.LIGHTRED_EX + "Invalid address. Please enter a valid address.")

    # Input birthday with validation
    while True:
        birthday = input(Fore.LIGHTYELLOW_EX + "Birthday (DD.MM.YYYY): " + Fore.RESET)
        if not birthday or validate_birthday(birthday):
            break
        print(Fore.LIGHTRED_EX + "Invalid birthday. Please enter in format DD.MM.YYYY")

    # Create a new record
    record = book.find(name)
    message = Fore.LIGHTGREEN_EX + "Contact updated." + Fore.RESET
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = Fore.LIGHTGREEN_EX + "Contact added." + Fore.RESET

    record.add_phone(phone)
    email and record.add_email(email)
    address and record.add_address(address)
    birthday and record.add_birthday(birthday)

    return message


def edit_contact(book: AddressBook) -> str:
    """Edit an existing contact by updating its fields."""

    name = suggest_name_input(
        "Enter the name of the contact you want to edit: ", book=book
    )

    # Find the record by name
    record = book.find(name)
    if record is None:
        return f"Contact with the name '{name}' not found."

    # Choose the field to edit
    field_to_edit = inquirer.select(
        message="Which field would you like to edit?",
        choices=["Phones", "Email", "Address", "Birthday", "Cancel"]
    ).execute()

    if field_to_edit == "Cancel":
        return "Edit operation cancelled."

    # Run the appropriate function to edit the field
    if field_to_edit == "Phones":
        phone_to_remove_edit = inquirer.select(
            message="Which phone would you like to edit/remove?",
            choices=['New'] + record.phones + ['Back']
        ).execute()

        if field_to_edit == "Back":
            return "Edit operation cancelled."

        if phone_to_remove_edit == "New":
            new_phone = input(Fore.LIGHTCYAN_EX + "Enter phone number to add: " + Fore.RESET)
        elif phone_to_remove_edit == "Back":
            return "Edit operation cancelled."
        else:
            new_phone = input(Fore.LIGHTCYAN_EX + "Enter the new phone or 'r' to remove: " + Fore.RESET)

        if new_phone is None:
            return "Edit operation cancelled."
        if new_phone == "r":
            record.remove_phone(phone_to_remove_edit)
            return "Phone number removed successfully."

        if phone_to_remove_edit == "New":
            record.add_phone(new_phone)
            return "Phone number added successfully."
        else:
            record.edit_phone(phone_to_remove_edit, new_phone)
            return "Phone number updated successfully."

    elif field_to_edit == "Email":
        new_email = input(Fore.LIGHTCYAN_EX + "Enter the new email address: " + Fore.RESET)
        record.edit_email(new_email)
        return record.get_info_with_title("Email address updated successfully.")

    elif field_to_edit == "Address":
        new_address = input(Fore.LIGHTCYAN_EX + "Enter the new address: " + Fore.RESET)
        record.edit_address(new_address)
        return record.get_info_with_title("Address updated successfully.")

    elif field_to_edit == "Birthday":
        new_birthday = input(Fore.LIGHTCYAN_EX + "Enter the new birthday (YYYY-MM-DD): " + Fore.RESET)
        record.add_birthday(new_birthday)
        return record.get_info_with_title("Birthday updated successfully.")


def main() -> None:
    """Main function to handle user input and commands."""
    print(Fore.GREEN + "Welcome to the assistant bot!")
    address_book_file = "var/addressbook.pkl"
    contacts, notes = load_data(address_book_file)
    while True:
        choice = inquirer.select(
            message="Choose an option:",
            choices=[
                "Add contact",
                "Change contact",
                "Delete contact",
                "Show all contacts",
                "Show birthday",
                "Show upcoming birthdays",
                "Search contacts",
                "Add note",
                "Change note",
                "Delete note",
                "Find note",
                "Show all notes",
                "Exit",
            ],
        ).execute()

        if choice == "Exit":
            save_data(contacts, notes, address_book_file)
            print("Good bye!")
            break
        elif choice == "Add contact":
            print(add_contact_interactive(contacts))
        elif choice == "Change contact":
            print(edit_contact(contacts))
        elif choice == "Delete contact":
            args = suggest_name_input(
                "Enter contact name to delete: ", book=contacts
            ).split()
            print(delete_contact(args, contacts))
        elif choice == "Show all contacts":
            print(show_all_contacts(contacts))
            print(show_all_contacts(args, contacts))
        elif choice == "Add birthday":
            args = input("Enter contact name and birthday: ").split()
            print(add_birthday(args, contacts))
        elif choice == "Show birthday":
            args = suggest_name_input("Enter contact name: ", book=contacts).split()
            print(show_birthday(args, contacts))
        elif choice == "Show upcoming birthdays":
            args = input("Enter number of days to check: ").split()
            print(birthdays(args, contacts))
        elif choice == "Search contacts":
            query = input("Enter search query: ")
            print(search_contacts(query, contacts))
        elif choice == "Add note":
            title = input("Enter a title: ")
            print(add_note(notes, title))
        elif choice == "Change note":
            title = input("Enter a title: ")
            print(change_note(notes, title))
        elif choice == "Delete note":
            title = input("Enter a title: ")
            print(delete_note(notes, title))
        elif choice == "Find note":
            title = input("Enter the title to search for: ")
            print(find_note(notes, title))
        elif choice == "Show all notes":
            print(show_all_notes(notes))
        elif choice == "add-tags":
            print(add_tags(args, contacts))
        elif choice == "remove-tags":
            print(remove_tags(args, contacts))
        else:
            print("Invalid command.")
        print()


if __name__ == "__main__":
    main()
