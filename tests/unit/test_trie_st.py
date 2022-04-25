"""
Tests for TrieST.py
"""
from pytest import fixture
from dirman.tree.TrieST import TrieST

@fixture
def trie_dict():
    trie = TrieST()
    d = {}
    s = ''
    for i in range(100):
        s += chr(ord('a') + i)
        for j in range(26):
            key = s + chr(ord('a') + j)
            trie.insert(key, i)
            d[key] = i
    return trie, d


def test_insert(trie_dict):
    """
    GIVEN a TrieST 
    WHEN insert is called with a key and value
    THEN the key and value are inserted into the TrieST
    """
    trie, d = trie_dict
    for k, v in d.items():
        assert v == trie.get(k).value


def test_delete(trie_dict):
    """
    GIVEN a TrieST 
    WHEN delete is called with a key
    THEN the key is deleted from the TrieST
    """
    trie, d = trie_dict
    assert len(d) == len(list(trie.matching_prefix('')))
    for k in list(d.keys()):
        trie.delete(k)
        del d[k]
    assert len(d) == len(list(trie.matching_prefix('')))


def test_matching_all_keys(trie_dict):
    """
    GIVEN a TrieST 
    WHEN matching_keys is called with an empty pattern
    THEN all keys are returned
    """
    trie, d = trie_dict
    for node in list(trie.matching_prefix('')):
        assert node.key in d
        del d[node.key]
    assert len(d) == 0


def test_matching_prefix(trie_dict):
    """
    GIVEN a TrieST 
    WHEN matching_keys is called with an empty pattern
    THEN all keys are returned
    """
    trie, d = trie_dict
    abc = [node.key for node in list(trie.matching_prefix('abc'))]
    actual_abc = [k for k in d.keys() if k.startswith('abc')]
    assert len(abc) == len(actual_abc)
    assert all(k in actual_abc for k in abc)