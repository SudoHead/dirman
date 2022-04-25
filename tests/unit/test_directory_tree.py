"""
Tests for DirectoryTree.py
"""
from pytest import fixture

from dirman.tree.info import FileType
from dirman.tree.DirectoryTree import DirectoryTree

@fixture
def tree():
    tree = DirectoryTree()
    tree.add('dataset')
    return tree


def test_add(tree):
    """
    GIVEN a DirectoryTree
    WHEN add is called with a directory name
    THEN the directory and its content is added to the DirectoryTree
    """
    assert tree._get_node(tree.root, 'dataset') is not None
    assert tree._get_node(tree.root, 'dataset').value == 'dataset'
    assert tree._get_node(tree.root, 'error') is None
    assert tree._get_node(tree.root, 'dataset/texts').value == 'texts'
    tests_subdir = tree._get_node(tree.root, 'dataset/texts').children.values()
    tests_subdir = [x.value for x in tests_subdir]
    for f in ['test1.txt', 'test2.txt', 'test3.txt']:
        assert f in tests_subdir


def test_delete(tree):
    """
    GIVEN a DirectoryTree
    WHEN delete is called with a directory name or file name
    THEN the content is deleted from the DirectoryTree
    """
    assert tree._get_node(tree.root, 'dataset/texts/test1.txt') is not None
    tree.delete('dataset/texts/test1.txt')
    assert tree._get_node(tree.root, 'dataset/texts/test1.txt').value is None
    assert tree._get_node(tree.root, 'dataset/texts') is not None
    tree.delete('dataset/texts')
    assert tree._get_node(tree.root, 'dataset/texts').value is None
    tree.delete('dataset')
    assert tree._get_node(tree.root, 'dataset/texts/test3.txt') is None
    assert tree._get_node(tree.root, 'dataset').value is None


def test_info(tree):
    """
    GIVEN a DirectoryTree
    WHEN info is called with a directory name or file name
    THEN the info object is correct
    """
    text = tree._get_node(tree.root, 'dataset/texts/test1.txt')
    assert text.info.type == FileType['text']

    image = tree._get_node(tree.root, 'dataset/images/binary_photo.jpg')
    assert image.info.type == FileType['image']

    text = tree._get_node(tree.root, 'dataset/texts/rainfall.py')
    assert text.info.type == FileType['text']