from .base_field import Field


class Tag(Field):
    def __init__(self, value: str):
        self.__validate(value)
        super().__init__(value)

    def __validate(self, value: str) -> None:
        length = len(value)
        if length < 3 or length > 10:
            raise ValueError("The tag should be between 3 and 10 characters long.")
