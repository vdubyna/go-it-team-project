from .base_field import Field


class Phone(Field):
    """A class for a field to store a phone number."""

    def __init__(self, number: str) -> None:
        self.value = self.validate_number(number)

    def validate_number(self, number: str) -> str:
        """Validate the phone number."""

        if len(number) != 10:
            raise ValueError("The phone number should have 10 digits only.")

        if not number.isdigit():
            raise ValueError("The phone number should have only numbers.")

        return number
