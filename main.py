import pickle
from fields.address_book import AddressBook
from fields.record import Record
from InquirerPy import inquirer
from colorama import init, Fore, Back, Style
from fields.validators import validate_name, validate_phone, validate_email, validate_address, validate_birthday
from decorators import input_error
from tabulate import tabulate

init(autoreset=True)

@input_error
def parse_input(user_input: str) -> tuple:
    """Parse user input into command and arguments."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def change_contact(args: list, book: AddressBook) -> str:
    """Update an existing contact in the address book."""
    if len(args) != 4:
        return "Invalid arguments. Usage: change-contact [name] [field] [old_value] [new_value]"

    name, field, old_value, new_value = args
    record = book.find(name)
    if record is None:
        return f"The record with name '{name}' is not found."

    field = field.lower()

    # Check if the given field is in the supported values
    if field not in {'name', 'email', 'phone', 'birthday'}:
        return f"Field '{field}' is not supported. Use 'name', 'email', 'phone' or 'birthday'."

    if field == "name":
        # Change the name of the record itself and the key in the contacts
        try:
            record.change_name(new_value)
            book.change_name(old_value, new_value)
        except KeyError as e:
            return str(e)

    elif field == "email":
        try:
            record.edit_email(old_value, new_value)
        except ValueError as e:
            return str(e)

    elif field == "phone":
        try:
            record.edit_phone(old_value, new_value)
        except ValueError as e:
            return str(e)

    elif field == "birthday":
        try:
            record.add_birthday(new_value)
        except ValueError as e:
            return str(e)

    return f"{field.capitalize()} changed!"


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
        name = input(Fore.LIGHTYELLOW_EX+ "Name: " + Fore.RESET)
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

    name = input("Enter the name of the contact you want to edit: ")

    # Find the record by name
    record = book.find(name)
    if record is None:
        return f"Contact with the name '{name}' not found."

    # Choose the field to edit
    field_to_edit = inquirer.select(
        message="Which field would you like to edit?",
        choices=["Phone", "Email", "Address", "Birthday", "Cancel"]
    ).execute()

    if field_to_edit == "Cancel":
        return "Edit operation cancelled."

    # Run the appropriate function to edit the field
    if field_to_edit == "Phone":
        old_phone = input(Fore.LIGHTMAGENTA_EX + "Enter the old phone number: " + Fore.RESET)
        new_phone = input(Fore.LIGHTCYAN_EX + "Enter the new phone number: " + Fore.RESET)
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated successfully."

    elif field_to_edit == "Email":
        new_email = input(Fore.LIGHTCYAN_EX + "Enter the new email address: " + Fore.RESET)
        record.edit_email(new_email)
        return "Email address updated successfully."

    elif field_to_edit == "Address":
        new_address = input(Fore.LIGHTCYAN_EX +  "Enter the new address: " + Fore.RESET)
        record.edit_address(new_address)
        return "Address updated successfully."

    elif field_to_edit == "Birthday":
        new_birthday = input(Fore.LIGHTCYAN_EX + "Enter the new birthday (YYYY-MM-DD): " + Fore.RESET)
        record.add_birthday(new_birthday)
        return "Birthday updated successfully."



def main() -> None:
    """Main function to handle user input and commands."""
    print(Fore.GREEN + "Welcome to the assistant bot!")
    address_book_file = "var/addressbook.pkl"
    contacts = load_data(address_book_file)

    while True:
        choice = inquirer.select(
            message= "Choose an option:",
            choices=[
                "Hello",
                "Add contact",
                "Change contact",
                "Delete contact",
                "Delete phone",
                "Show phone number",
                "Show all contacts",
                "Add birthday",
                "Show birthday",
                "Show upcoming birthdays",
                "Search contacts",
                "Exit",
            ],
        ).execute()

        if choice == "Exit":
            save_data(contacts, address_book_file)
            print("Good bye!")
            break
        elif choice == "Hello":
            print("How can I help you?")
        elif choice == "Add contact":
            print(add_contact_interactive(contacts))
        elif choice == "Change contact":
            print(edit_contact(contacts))
        elif choice == "Show phone number":
            args = input("Enter contact name: ").split()
            print(change_contact(args, contacts))
        elif choice == "Delete contact":
            args = input("Enter contact name to delete: ").split()
            print(delete_contact(args, contacts))
        elif choice == "Delete phone":
            args = input("Enter phone to delete: ").split()
            print(show_phone(args, contacts))
        elif choice == "Show all contacts":
            print(show_all_contacts(contacts))
        elif choice == "Add birthday":
            args = input("Enter contact name and birthday: ").split()
            print(add_birthday(args, contacts))
        elif choice == "Show birthday":
            args = input("Enter contact name: ").split()
            print(show_birthday(args, contacts))
        elif choice == "Show upcoming birthdays":
            args = input("Enter number of days to check: ").split()
            print(birthdays(args, contacts))
        elif choice == "Search contacts":
            query = input("Enter search query: ")
            print(search_contacts(query, contacts))
        print()


if __name__ == "__main__":
    main()
