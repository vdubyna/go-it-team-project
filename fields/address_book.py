from datetime import datetime, timedelta
from collections import UserDict
from typing import Optional
from tabulate import tabulate

from .record import Record
from .base_collection import BaseCollection


class AddressBook(UserDict, BaseCollection[Record]):
    """Implementation of basic version of the address book."""

    def add(self, record: Record) -> None:
        """Add the record to the address book."""
        if record.name.value in self.data:
            raise KeyError(f"The record with name '{record.name.value}' already exists.")

        self.data[record.name.value] = record

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
                        birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))

                    upcoming_birthdays.append(f"{user.name.value}: {birthday_this_year.strftime('%d.%m.%Y')}")

        return "\n".join(upcoming_birthdays)
    
    def get_all(self):
        return list(self.data.values())
    
    def _match_entity(self, record: Record, query: str, tag: str = "") -> Record | None:
        """Check if the record matches the query."""
        if tag and not record.includes_tag(tag):
            return None
        if query:
            if query in record.name.value.lower():
                return record
            for phone in record.phones:
                if query in phone.value:
                    return record
            if record.email and query in record.email.value.lower():
                return record
            if record.address and query in record.address.value.lower():
                return record
            if record.birthday and query in record.birthday.value.lower():
                return record
            return None
        return record
    
    def render_table(self, records: list[Record], no_data_str: str) -> str:
        if not records:
            return tabulate([[no_data_str]], tablefmt="grid")
        table = []
        for record in records:
            phones = "; ".join(phone.value for phone in record.phones)
            email = record.email.value if record.email else "N/A"
            address = record.address.value if record.address else "N/A"
            birthday = record.birthday.date.strftime("%d.%m.%Y") if record.birthday else "N/A"
            tags = "; ".join(tag.value for tag in record.tags) if record.tags else "N/A"

            table.append([record.name.value, phones, email, address, birthday, tags])

        return tabulate(table, headers=["Name", "Phone", "Email", "Address", "Birthday", "Tags"], tablefmt="grid")
