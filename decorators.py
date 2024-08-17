from colorama import Fore


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return Fore.RED + str(e)
        except KeyError as e:
            return Fore.RED + str(e)
        except IndexError as e:
            return Fore.RED + str(e)

    return inner
