from .base_entity import BaseEntity
from .base_field import Field


class Title(Field):
    """A class for a field to store a title of a note."""

    def __init__(self, value: str) -> None:
        if not value:
            raise ValueError("Note title should not be empty.")
        if len(value) > 100:
            raise ValueError("Note title should not be longer than 100 characters.")
        super().__init__(value)


class Content(Field):
    """A class for a field to store a content of a note."""

    def __init__(self, value: str = "") -> None:
        if len(value) > 200:
            raise ValueError("Note title should not be longer than 200 characters.")
        super().__init__(value)


class Note(BaseEntity):
    """A class for a field to store a note as a separate object."""

    def __init__(self, title: str, content: str = "", tags: list[str] = []) -> None:
        self.title = Title(title)
        self.content = Content(content)
        super().__init__()

    def __str__(self) -> str:
        title_str = f"Title: {self.title.value}"
        content_str = f"Content: {self.content}" if self.content else "n/a"
        tags_str = f"Tags: {"; ".join(t.value for t in getattr(self, "tags", [])) or "n/a"}"
        return "\n".join([title_str, content_str, tags_str])
    
    def add_content(self, value: str = ""):
        self.content = Content(value)


class Notes:
    def __init__(self) -> None:
        self.notes: list = []

    def find_note(self, title: str) -> Note | None:
        if not title:
            raise ValueError("Title is required")

        for note in self.notes:
            if note.title.value == title:
                return note
        return None

    def add_note(self, title: str, text=None) -> str:
        note = Note(title, text)
        self.notes.append(note)
        return f"Note with title: '{title}' added."

    def delete_note(self, title: str) -> str:
        if not (note := self.find_note(title)):
            return f"Note with title: '{title}' is not found."

        self.notes.remove(note)
        return f"Note with title: '{title}' deleted."

    def show_all(self) -> str:
        if not self.notes:
            return "No notes available."

        divider = "-" * 40
        return "\n\n".join(f"{divider}\n{note}\n{divider}" for note in self.notes)
