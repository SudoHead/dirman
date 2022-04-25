"""
Tests for commands.py
"""
from pytest import fixture, raises
from dirman import commands

def foo(a, b, c):
    print('foo')
    return [a, b, c]

def bar(a, b, c = None, d = None):
    return [a, b, c, d]

@fixture
def cmd():
    commands.COMMAND_TO_HANDLER = {
        'foo': foo,
        'bar': bar,
    }


def test_foo(cmd):
    """
    GIVEN a command
    WHEN handle_command is called
    THEN the command is executed and returns the intended result
    """
    command = 'foo a b c'
    assert commands.handle_command(command) == ['a', 'b', 'c']

    command = 'foo a b c d'
    assert commands.handle_command(command) == None


def test_bar(cmd):
    """
    GIVEN a command
    WHEN handle_command is called with missing optional arguments
    THEN the command is executed anyway
    """
    command = 'bar a b'
    assert commands.handle_command(command) == ['a', 'b', None, None]

    command = 'bar a b c'
    assert commands.handle_command(command) == ['a', 'b', 'c', None]

    command = 'bar a b c d'
    assert commands.handle_command(command) == ['a', 'b', 'c', 'd']

    command = 'bar a b c d e'
    assert commands.handle_command(command) == None