from decorators import input_error
from models.errors import FlagArgInvalid, FlagInvalid


@input_error
def parse_input(user_input: str) -> tuple:
    """Parse user input into command and arguments."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def parse_flags(args: list[str], acceptable: list[str]) -> tuple[dict, list[str]]:
    """Parse flags from the arguments."""
    flags = {}
    skipped: list[str] = []
    for i, arg in enumerate(args):
        # Skip the argument if it was already processed with the flag
        if not arg.startswith('-'):
            prev = args[i - 1]
            if prev and not prev.startswith('-'):
                skipped.append(arg) # not included in the flags
            continue
        flag = arg.lstrip('-')
        if flag not in acceptable:
            raise FlagInvalid(f"Invalid flag '{flag}'")
        flag_arg = args[i + 1]
        if not flag_arg or flag_arg.startswith('-'):
            raise FlagArgInvalid(f"Invalid argument '{flag_arg}' for flag '{flag}'")
        flags[flag] = flag_arg
    return flags, skipped