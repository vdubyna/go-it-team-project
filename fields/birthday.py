from .base_field import Field
from datetime import datetime


class Birthday(Field):
    """A class for a field to store a birthday date."""

    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)
