from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from fields.address_book import AddressBook


def suggest_name_input(text: str, book: AddressBook):
    command_completer = WordCompleter(list(book.data), ignore_case=True)
    session = PromptSession(completer=command_completer)
    return session.prompt(text)
