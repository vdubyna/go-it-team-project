from .phone import Phone
from .name import Name
from .birthday import Birthday


class Record:
    """A class for a contact record that contains a name and a list of phone numbers."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday = None

    def __str__(self) -> str:
        return f"Contact name: {self.name.value} || phones: {'; '.join(p.value for p in self.phones)} || birthday: {self.birthday}"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, number: str) -> None:
        """Add a phone number to the record."""
        self.phones.append(Phone(number))

    def remove_phone(self, number: str) -> None:
        """Remove a phone number from the record."""
        self.phones = [phone for phone in self.phones if phone.value != number]

    def edit_phone(self, old_number: str, new_number: str) -> None:
        """Edit a phone number in the record."""
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                break
        return None

    def find_phone(self, number: str) -> Phone | None:
        """Find a phone number in the record."""
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None
