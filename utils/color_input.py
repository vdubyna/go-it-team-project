from colorama import init, Fore

init(autoreset=True)


def color_input(msg: str):
    return input(Fore.LIGHTYELLOW_EX + msg + Fore.RESET)