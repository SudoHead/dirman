"""
A symbol table implementation using a Trie data structure.
"""

from queue import Queue
from typing import Iterator, Tuple
from dirman.tree.TreeNode import TreeNode
from dirman.tree.info import DirInfo, FileInfo

class TrieST:
    def __init__(self):
        self.root = TreeNode()


    def insert(
            self, 
            key: str, 
            value: str, 
            is_dir: bool = False, 
            root: bool = False,
        ) -> Tuple[bool, TreeNode]:
        """
        Adds a key-value pair to the TrieST.

        Args:
            key (str): The string key to add.
            value (str): Value of the key.
            is_dir (bool, optional): is key a directory. Defaults to False.
            root (bool, optional): is key the root directory. Defaults to False.

        Returns:
            Tuple[bool, TreeNode]: (True, node) if a new key is inserted,
                (False, node) if key is updated (already exists).
        """
        self._key_valid(key)
        node = self.root
        is_new_key = False
        for char in key:
            if char not in node.children:
                is_new_key = True
                node.children[char] = TreeNode()
            node = node.children[char]
        node.key = key
        node.value = value
        node.is_dir = is_dir
        return is_new_key, node
    

    def delete(self, key: str):
        """
        Deletes the subtree rooted at the key.

        Args:
            key (str): the key to delete.
        """
        self._key_valid(key)
        node = self.root
        for char in key:
            if char not in node.children:
                return
            node = node.children[char]
        node.reset()

    
    def get(self, key: str) -> TreeNode:
        """
        Returns the node associated with the key.

        Args:
            key (str): the key to search for.

        Returns:
            TreeNode: the node associated with the key.
        """
        if not key:
            return self.root
        node = self.root
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        return node


    def matching_prefix(self, prefix) -> Iterator[TreeNode]:
        """
        Returns an iterator over the nodes with the given prefix.

        Args:
            prefix (str): the prefix to match.

        Yields:
            Iterator[TreeNode]: generator of nodes with the given prefix.
        """
        q = Queue()
        node = self.get(prefix)
        self._matching_prefix(node, q)
        while not q.empty():
            yield q.get()


    def _matching_prefix(self, node, results_queue):
        """
        Helper function for matching_prefix.
        """
        if not node:
            return
        if node.value is not None and not node.is_dir:
            results_queue.put(node)
        for child in node.children:
            self._matching_prefix(node.children[child], results_queue)

    def _key_valid(self, key):
        if not key:
            raise ValueError("key cannot be null or empty")
