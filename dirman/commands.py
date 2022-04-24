"""
This module contains functions to process and map string commands,
and then call the appropriate handler function.

Command mapping must be supplied to COMMAND_TO_HANDLER.
"""
import inspect
from typing import Tuple

COMMAND_TO_HANDLER = {}


def split_command_and_args(tokens: list[str]) -> \
    Tuple[str, list[str], dict[str, str]]:
    """Splits the command and its arguments. 
    When an option type is detected (starting with '-'), it is matched 
    with the next argument if possible. If not, it is treated as a boolean.

    Args:
        tokens: list of tokens to process

    Returns:
        (command, positional_args, args)
    """
    cmd = tokens.pop(0)
    args = {}
    positional = []
    while tokens:
        token = tokens.pop(0)
        if token.startswith('-'):
            # match with next token
            token = token.lstrip('-')
            if tokens and not tokens[0].startswith('-'):
                args[token] = tokens.pop(0)
            else:
                args[token] = True
        # if no option type specified: it is a positional argument
        else:
            positional.append(token)
    return cmd, positional, args


def handle_command(input_string: str) -> None:
    """
    Handles the input command and calls its handler.
    """
    input_string = input_string.strip()
    if not input_string:
        print('input string is empty')
        return

    tokens = input_string.split()
    cmd, positional, args = split_command_and_args(tokens)
    
    try:
        handler = COMMAND_TO_HANDLER[cmd]
    except KeyError:
        print(f"unknown command: {cmd}")
        return
    # calles the command's handler function
    try:
        handler(*positional, **args)
    except TypeError:
        expected_args = inspect.signature(handler).parameters.keys()
        print(f"Command [{cmd}] takes ({', '.join(expected_args)}) " + \
            f"arguments but ({', '.join(positional)}) were given")
        return


if __name__ == "__main__":
    input_string = input("Enter command: ")
    def show(folder, folder2, **kwargs):
        print(folder, folder2)
        print(kwargs)
    COMMAND_TO_HANDLER = {'filter': show}
    handle_command(input_string)