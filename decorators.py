from models.errors import FlagArgInvalid, FlagInvalid


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid arguments. Please, provide name and phone number."
        except KeyError:
            return "Contact does not exist."
        except IndexError:
            return "Invalid arguments. Please, provide name."
        except (FlagInvalid, FlagArgInvalid) as e:
            return e

    return inner
