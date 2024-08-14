from .base_field import Field


class Address(Field):
    """A class for a field to store a physical address."""

    def __init__(self, value):
        if not self._is_valid_address(value):
            raise ValueError("Invalid address format.")
        self.value = value

    @staticmethod
    def _is_valid_address(address):
        """Basic validation for address."""
        return len(address.strip()) > 0
