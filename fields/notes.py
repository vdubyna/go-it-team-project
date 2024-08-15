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

