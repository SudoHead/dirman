"""
A symbol table implementation using a Trie data structure.
"""

from queue import Queue
from typing import Tuple
from dirman.tree.TreeNode import TreeNode

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
        tree_level = 1
        is_new_key = False
        for char in key:
            if char not in node.children:
                is_new_key = True
                node.children[char] = TreeNode(tree_level = tree_level)
            if node.children[char].is_dir:
                tree_level += 1
            node = node.children[char]
        node.value = value
        node.is_dir = is_dir
        if root:
            node.tree_level = 0
        return is_new_key, node
    

    def delete(self, key):
        self._key_valid(key)
        node = self.root
        for char in key:
            if char not in node.children:
                return
            node = node.children[char]
        node.reset()

    
    def get(self, key):
        self._key_valid(key)
        node = self.root
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.value


    def starts_with(self, prefix):
        self._key_valid(prefix)
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


    def matching_prefix(self, prefix):
        q = Queue()
        self._matching_prefix(self.root, [], q)
        while not q.empty():
            yield q.get()


    def _matching_prefix(self, node, prefix, results_queue):
        if not node:
            return
        if node.value:
            results_queue.put(node)
        for child in node.children:
            prefix.append(child)
            self._matching_prefix(node.children[child], prefix, results_queue)
            prefix.pop()


    def matching_pattern(self, pattern):
        q = Queue()
        self._matching_pattern(self.root, [], pattern, q)
        while not q.empty():
            yield q.get()


    def _matching_pattern(self, node, prefix, pattern, results_queue):
        if not node:
            return
        l = len(prefix)
        if l == len(pattern) and node.value != None:
            results_queue.put(''.join(prefix))
        if l == len(pattern):
            return
        c = pattern[l]
        if c == '*':
            for child in node.children:
                prefix.append(child)
                self._matching_pattern(node.children[child], prefix, pattern, results_queue)
                prefix.pop()
        else:
            prefix.append(c)
            self._matching_pattern(node.children[c], prefix, pattern, results_queue)
            prefix.pop()


    def _key_valid(self, key):
        if not key:
            raise ValueError("key cannot be null or empty")


if __name__ == '__main__':
    q = Queue()
    q.put(1)
    q.put(2)
    q.put(3)
    q.put(4)

    while not q.empty():
        print(q.get())
