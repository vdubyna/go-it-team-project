from .base_field import Field
import re


class Email(Field):
    """A class for a field to store an email address."""

    def __init__(self, value):
        if not self._is_valid_email(value):
            raise ValueError("Invalid email address format.")
        self.value = value

    @staticmethod
    def _is_valid_email(email):
        """Validate the email address format."""
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return re.match(pattern, email) is not None
