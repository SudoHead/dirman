"""
Tests for TrieST.py
"""
from pytest import fixture
from dirman.TrieST import TrieST

@fixture
def trie_dict():
    trie = TrieST()
    d = {}
    s = ''
    for i in range(256):
        s += chr(i)
        for j in range(26):
            key = s + chr(j)
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
        assert v == trie.get(k)


def test_delete(trie_dict):
    """
    GIVEN a TrieST 
    WHEN delete is called with a key
    THEN the key is deleted from the TrieST
    """
    trie, d = trie_dict
    for k in list(d.keys()):
        trie.delete(k)
        del d[k]
    assert len(d) == len(list(trie.matching_keys('')))


def test_matching_all_keys(trie_dict):
    """
    GIVEN a TrieST 
    WHEN matching_keys is called with an empty pattern
    THEN all keys are returned
    """
    trie, d = trie_dict
    for k in trie.matching_keys('*'):
        assert k in d
        del d[k]
    assert len(d) == 0