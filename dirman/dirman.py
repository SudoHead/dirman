import click
import prompt_toolkit as cli
from dirman.tree.TrieST import TrieST
from dirman.tree.DirectoryTree import DirectoryTree
import dirman.commands as commands
import inspect, functools
import math

prompt_history = cli.history.InMemoryHistory()
prompt_session = cli.PromptSession(history = prompt_history)

directory_tree = DirectoryTree()


def command(func = None, name = None, help = None):
    """Decorator to link the command function to its handler."""
    if func is None:
        return functools.partial(command, name = name, help = help)

    @functools.wraps(func)
    def decorator_command(name): # the actual decorator
        commands.COMMAND_TO_HANDLER.update(
            {name if name else func.__name__: func})
    return decorator_command(name)


@command
def add(directory: str):
    directory_tree.add(directory)


@command
def delete(path: str):
    print("Deleting:", path)
    directory_tree.delete(path)


@command
def view(directory: str = ''):
    print("Viewing: ", directory)
    directory_tree.view(directory)


@command
def filter(directory, prefix = '', type = None, gt = None, lt = None):
    print("Filtering: ", directory)
    if not gt:
        gt = -1
    else:
        gt = commands.convert_num(gt)
    if not lt:
        lt = math.inf
    else:
        lt = commands.convert_num(lt)
    directory_tree.filter(
        directory, prefix, 
        **{'type': type, 'gt': gt, 'lt': lt})


@command
def save():
    print("I am save!")


@command
def exit():
    print("Exiting the dirman.py... Goodbye!")
    quit()


@command
def clear():
    cli.shortcuts.clear()


@command
def help():
    click.echo("Available commands:")
    for cmd, func in commands.COMMAND_TO_HANDLER.items():
        parameters = inspect.signature(func).parameters.keys()
        click.echo(f" - {cmd} {' '.join(parameters)}")


@command
def history():
    hist = prompt_history.get_strings()
    num_padding = len(str(len(hist)))
    for i, cmd in enumerate(hist, 1):
        click.echo(f"{i:>{num_padding}}  {cmd}")


@command(name = '!')
def repeat_history(history_index: int):
    try:
        history_index = int(history_index)
    except ValueError:
        print("history_index must be an integer.")
        return
    hist = prompt_history.get_strings()
    if history_index < 1 or history_index > len(hist):
        click.echo(f"Invalid history index: {history_index}")
        return
    print(hist[history_index - 1])
    commands.handle_command(hist[history_index - 1])


def main():
    while True:
        try:
            text = prompt_session.prompt('> ')
            commands.handle_command(text)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
    print('Execution interupted!')


if __name__ == '__main__':
    main()