from datetime import datetime, timedelta
from collections import UserDict
from typing import Optional

from .record import Record


class AddressBook(UserDict):
    """Implementation of basic version of the address book."""

    def add_record(self, record: Record) -> None:
        """Add the record to the address book."""
        if record.name.value in self.data:
            raise KeyError(f"The record with name '{record.name.value}' already exists.")

        self.data[record.name.value] = record

    def change_name(self, old_name, new_name):
        """Change the name of the record in the address book."""
        if old_name not in self.data:
            raise KeyError(f"The record with name '{old_name}' is not found.")

        # Change the key for the existing record
        current_record = self.data[old_name]
        self.data[new_name] = current_record
        self.delete(old_name)

    def find(self, name: str) -> Optional[Record]:
        """Find the record by name."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Delete the record by name."""
        if name not in self.data:
            raise KeyError(f"The record with name '{name}' is not found.")

        del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for user in self.data.values():
            if user.birthday:
                # Convert the birthday string to a datetime.date object
                birthday_date = datetime.strptime(user.birthday.value, "%d.%m.%Y").date()
                # Set the year to the current year to be able to compare with the current date
                birthday_this_year = birthday_date.replace(year=today.year)

                # If the birthday has passed this year, move it to next year
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                # Get the number of days until the next birthday
                days_until_birthday = (birthday_this_year - today).days

                if 0 <= days_until_birthday <= 7:
                    if birthday_this_year.weekday() >= 5:
                        birthday_this_year += timedelta(
                            days=(7 - birthday_this_year.weekday())
                        )

                    upcoming_birthdays.append(
                        f"{user.name.value}: {birthday_this_year.strftime('%d.%m.%Y')}"
                    )

        return "\n".join(upcoming_birthdays)

    def get_records(self, sort: str = "name", order: str = "asc", tag: str = "") -> list[Record]:
        """Get the records sorted by the passed parameter."""
        records: list[Record] = list(self.data.values())
        if tag:
            records = [record for record in records if record.includes_tag(tag)]
        return sorted(
            records,
            key=lambda record: getattr(record, sort).value,
            reverse=False if order == "asc" else True,
        )
        
