import pickle
from fields.address_book import AddressBook
from fields.base_entity import BaseEntity
from fields.record import Record
from InquirerPy import inquirer
from colorama import init, Fore
from fields.validators import validate_name, validate_phone, validate_email, validate_address, validate_birthday, validate_tags
from fields.notes import Note, Notes
from decorators import input_error
from utils import suggest_name_input, color_input

init(autoreset=True)

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
        return Fore.RED + "Invalid number of arguments. Usage: delete-contact [name]"

    name = args[0]
    record = book.find(name)
    if record:
        book.delete(name)
        return Fore.GREEN + f"Contact '{name}' successfully deleted"

    return Fore.YELLOW + f"No contact with the name '{name}' exists"


def show_all_contacts(book: AddressBook) -> str:
    """Show all contacts in a formatted table."""
    return book.render_table(list(book.data.values()), no_data_str="Contacts are empty.")


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
def add_tags(book: AddressBook):
    name, *_ = suggest_name_input("Enter contact name: ", book).split()
    record = book.find(name)
    if record is None:
        return f"The record with name '{name}' is not found."
    tags = color_input("Enter tags: ").split()
    record.add_tags(tags)
    return "Tags added."


@input_error
def remove_tags(book: AddressBook):
    name, *_ = suggest_name_input("Enter contact name: ", book).split()
    record = book.find(name)
    if record is None:
        return f"The record with name '{name}' is not found."
    tags = color_input("Enter tags: ").split()
    record.add_tags(tags)
    record.remove_tags(tags)
    return "Tags removed."


@input_error
def add_note(notes: Notes) -> str:
    """Add a new note to notes."""
    title = input("Enter a title: ")
    if notes.find_note(title):
        return f"Note with title '{title}' already exists."

    text = input("Enter a text: ")
    try:
        message = notes.add_note(title, text)
        return message
    except ValueError as e:
        return str(e)


@input_error
def change_note(notes: Notes) -> str:
    """Change the existing note by its title."""
    title = input("Enter a title: ")
    entity = notes.find_note(title)
    if not entity:
        return f"Note with title: '{title}' is not found."

    choice = inquirer.select(
        message="Which field would you like to edit?",
        choices=["Content", "Tags", "Cancel"]
    ).execute()

    if choice == "Cancel":
        return "Operation cancelled."
    elif choice == "Content":
        value = color_input("Enter new content: ")
        entity.add_content(value)
        return f"Content edited successfully."
    elif choice == "Tags":
        return edit_tag(entity)


@input_error
def delete_note(notes: Notes) -> str:
    """Delete the existing note by its title."""
    title = input("Enter a title: ")

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
    return notes.render_table(notes.get_all(), no_data_str="No notes available.")

@input_error
def search_notes(notes: Notes) -> str:
    query = color_input("Enter search query: ")
    tag = color_input("Enter tag (optional): ")

    order = inquirer.select(
        message="Order: ",
        choices=["asc", "desc"],
    ).execute()

    results: list[Note] = notes.search(query, tag, "title", order)
    return notes.render_table(results, no_data_str="No matching notes found.")


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
def search_contacts(book: AddressBook) -> str:
    """Search for contacts by any field."""
    query = color_input("Enter search query: ")
    tag = color_input("Enter tag (optional): ")

    order = inquirer.select(
        message="Order: ",
        choices=["asc", "desc"],
    ).execute()

    results: list[Record] = book.search(query, tag, "name", order)
    return book.render_table(results, no_data_str="No matching contacts found.")


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

    # Input tags
    while True:
        tags = input(Fore.LIGHTYELLOW_EX + "Tags: " + Fore.RESET).split()
        if not tags or validate_tags(tags):
            break
        print(Fore.LIGHTRED_EX + f"Invalid tags. The tag should be between 3 and 10 characters long.")
        


    # Create a new record
    record = book.find(name)
    message = Fore.LIGHTGREEN_EX + "Contact updated." + Fore.RESET
    if record is None:
        record = Record(name)
        book.add(record)
        message = Fore.LIGHTGREEN_EX + "Contact added." + Fore.RESET

    record.add_phone(phone)
    email and record.add_email(email)
    address and record.add_address(address)
    birthday and record.add_birthday(birthday)
    tags and record.add_tags(tags)

    return message

def edit_tag(record: BaseEntity):
        choiced = inquirer.select(
            message="Which tag would you like to edit/remove?",
            choices=['New'] + record.tags + ['Back']
        ).execute()
        if choiced == "Back":
            return "Operation cancelled."
        elif choiced == "New":
            value = color_input("Enter name to add: ")
            record.add_tags([value])
            return f"Tag '{value}' added successfully."
        else:
            selected_tag = choiced
            input_value = color_input("Enter new name or 'r' to remove: ")
            record.remove_tags([selected_tag.value])
            if input_value == "r":
                return f"Tag '{selected_tag}' removed successfully."
            else:
                record.add_tags([input_value])
                return f"Tag '{selected_tag}' renamed into '{input_value}' successfully."


@input_error
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
        choices=["Phones", "Email", "Address", "Birthday", "Tags", "Cancel"]
    ).execute()

    if field_to_edit == "Cancel":
        return "Edit operation cancelled."

    # Run the appropriate function to edit the field
    if field_to_edit == "Phones":
        phone_to_remove_edit = inquirer.select(
            message="Which phone would you like to edit/remove?",
            choices=['New'] + record.phones + ['Back']
        ).execute()

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
    
    elif field_to_edit == "Tags":
        return edit_tag(record)


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
                "Search notes",
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
            args = suggest_name_input("Enter contact name to delete: ", book=contacts).split()
            print(delete_contact(args, contacts))
        elif choice == "Show all contacts":
            print(show_all_contacts(contacts))
        elif choice == "Show birthday":
            args = suggest_name_input("Enter contact name: ", book=contacts).split()
            print(show_birthday(args, contacts))
        elif choice == "Show upcoming birthdays":
            args = input("Enter number of days to check: ").split()
            print(birthdays(args, contacts))
        elif choice == "Search contacts":
            print(search_contacts(contacts))
        elif choice == "Add note":
            print(add_note(notes))
        elif choice == "Change note":
            print(change_note(notes))
        elif choice == "Delete note":
            print(delete_note(notes))
        elif choice == "Find note":
            title = input("Enter the title to search for: ")
            print(find_note(notes, title))
        elif choice == "Show all notes":
            print(show_all_notes(notes))
        elif choice == "Search notes":
            print(search_notes(notes))
        print()


if __name__ == "__main__":
    main()
