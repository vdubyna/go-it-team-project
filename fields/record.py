from .phone import Phone
from .name import Name
from .birthday import Birthday
from .email import Email
from .address import Address


class Record:
    """A class for a contact record that contains a name and a list of phone numbers."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.address: Address | None = None
        self.email: Email | None = None
        self.birthday: str | None = None

    def __str__(self) -> str:
        return f"Contact name: {self.name.value} || phones: {'; '.join(p.value for p in self.phones)} || birthday: {self.birthday} || email: {self.email} || address: {self.address}"

    def add_birthday(self, birthday):
        """Add a birthday to the record."""
        self.birthday = Birthday(birthday)

    def add_phone(self, number: str) -> None:
        """Add a phone number to the record."""
        self.phones.append(Phone(number))

    def remove_phone(self, number: str) -> None:
        """Remove a phone number from the record."""
        self.phones = [phone for phone in self.phones if phone.value != number]

    def edit_phone(self, old_number: str, new_number: str) -> None:
        """Edit a phone number in the record."""
        found = False

        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                found = True
                break

        if not found:
            raise ValueError("The specified number does not exist or there are no phone numbers for the contact.")

    def find_phone(self, number: str) -> Phone | None:
        """Find a phone number in the record."""
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None

    def change_name(self, new_name: str) -> None:
        self.name = Name(new_name)

    def add_email(self, email: str) -> None:
        """Add an email address to the record."""
        self.email = Email(email)

    def edit_email(self, new_email: str) -> None:
        """Edit the email address in the record."""
        self.email = Email(new_email)

    def add_address(self, address: str) -> None:
        """Add a physical address to the record."""
        self.address = Address(address)

    def edit_address(self, new_address: str) -> None:
        """Edit the physical address in the record."""
        self.address = Address(new_address)

    def get_info_with_title(self, title: str) -> str:
        """Make readable info with current record state and title."""
        return title + "\n" + str(self)
