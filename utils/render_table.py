from fields.record import Record
from tabulate import tabulate


def render_table(records: list[Record]):
    table = []
    for record in records:
        phones = "; ".join(phone.value for phone in record.phones)
        email = record.email.value if record.email else "N/A"
        address = record.address.value if record.address else "N/A"
        birthday = record.birthday.date.strftime("%d.%m.%Y") if record.birthday else "N/A"
        tags = "; ".join(tag.value for tag in record.tags) if record.tags else "N/A"

        table.append([record.name.value, phones, email, address, birthday, tags])

    return tabulate(table, headers=["Name", "Phone", "Email", "Address", "Birthday", "Tags"], tablefmt="grid")