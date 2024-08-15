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

    def __init__(self, value: str) -> None:
        if len(value) > 200:
            raise ValueError("Note title should not be longer than 200 characters.")
        super().__init__(value)


class Note:
    """A class for a field to store a note as a separate object."""

    def __init__(self, title: str, content: str | None = None) -> None:
        self.title = Title(title)
        self.content = Content(content)

    def __str__(self) -> str:
        title_str = f"Title: {self.title.value}"
        content_str = f"Content: {self.content}" if self.content else ""
        # Return title + content if the content is present or just title otherwise
        return f"{title_str}\n{content_str}" if content_str else title_str


class Notes:
    def __init__(self) -> None:
        self.notes: list = []

    def find_note(self, title: str) -> str | None:
        if not title:
            raise ValueError("Title is required")

        for note in self.notes:
            if note.title.value == title:
                return note
        return None

    def add_note(self, title: str, text=None) -> str:
        if self.find_note(title):
            raise ValueError(f"Note with title as '{title}' exists already.")

        note = Note(title, text)
        self.notes.append(note)
        return f"Note with title: '{title}' added."

    def change_note(self, title: str, new_content: str) -> str:
        if not (note := self.find_note(title)):
            return f"Note with title: '{title}' is not found."

        note.content = Content(new_content) if new_content else note.content
        return f"Note with title: '{title}' changed."

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
