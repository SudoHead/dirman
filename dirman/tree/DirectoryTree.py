from dirman.tree.TreeNode import TreeNode
from dirman.tree.TrieST import TrieST
import pathlib, os
from dirman.tree.info import DirInfo, FileInfo
import rich
from rich.console import Console
from rich.table import Table
from queue import Queue

rconsole = Console()

def path_not_exist_error(path):
    rconsole.print(
        f"{path} does not exist.", 
        style = "bold red")


class DirectoryTree:
    def __init__(self):
        self.root = TreeNode(None, None, None, None)
        self.trie = TrieST()
        self.added_dirs = []


    def add(self, directory: str):
        """Adds the input directory and its content to the directory tree.

        Args:
            directory (str): The directory to add.
        """
        total_size = self._radd(directory)
        path = pathlib.Path(directory)
        if path.is_dir:
            root_node = self.insert(self.root, str(path), total_size, is_dir = True)
            self.added_dirs.append(root_node)


    def _radd(self, directory: str) -> int:
        """Recursively adds the directory and its content to the directory tree.
        
        Args:
            directory (str): the directory to add.

        Returns:
            int: Return the total size of the directory.
        """
        if not os.path.exists(directory):
            path_not_exist_error(directory)
            return 0

        path = pathlib.Path(directory)
        
        total_size = 0
        for p in path.glob('*'):
            if p.name.startswith('.'): # avoid hidden files
                continue
            if p.is_dir():
                total_size += self._radd(str(p))
            size = p.stat().st_size
            total_size += size
            ins_node = self.insert(self.root, str(p), size, is_dir = p.is_dir())
            # update the trie reference
            if not p.is_dir():
                node = self.trie.get(p.name)
                if node is None:
                    self.trie.insert(p.name, [ins_node])
                else:
                    node.value.append(ins_node)
        return total_size


    def delete(self, path):
        """Deletes the input path from the directory tree.

        Args:
            path (str): path can be a directory or a file.
        """
        node = self.get_node(self.root, path)
        if node is None:
            path_not_exist_error(path)
            return
        q = Queue()
        q.put(node)
        while not q.empty():
            x = q.get()
            for child in x.children.values():
                q.put(child)
            x.reset()
            try:
                self.trie.delete(x.value)
            except ValueError:
                pass


    def view(self, directory: str = '', **kwargs):
        if not directory:
            self.table_view(**kwargs)
            return
        
        subtree = self.get_node(self.root, directory)
        if subtree is None:
            path_not_exist_error(directory)
            return
        rich.print(subtree.view_tree(**kwargs))


    def table_view(self, **kwargs):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Directory", style="bold magenta")
        table.add_column("upload time" , style="dim")
        table.add_column("last accessed", style="dim")
        table.add_column("size", justify="right")

        for node in self.added_dirs:
            table.add_row(
                node.value,
                node.info.upload_time,
                node.info.last_accessed,
                node.info.humansize(),
            )
        rconsole.print(table)


    def filter(self, directory: str = '', prefix: str = '', *args, **kwargs):
        """
        Filters the directory tree based on the input prefix.

        Args:
            directory (str, optional): where to filter. Defaults to ''.
            prefix (str, optional): prefix pattern. Defaults to ''.
        """
        ftree = TreeNode()
        # search with a trie
        if prefix: 
            prefix = prefix.replace("*", "")
            node_gen = self.trie.matching_prefix(prefix)

            while True:
                try:
                    node = next(node_gen)
                    for x in node.value:
                        fnode = self.insert(ftree, x.key, is_dir = x.is_dir)
                        fnode.info = x.info
                except StopIteration:
                    break
        else:
            ftree = self.root

        # view the filtered tree
        subtree = self.get_node(ftree, directory)
        if subtree is None:
            path_not_exist_error(directory)
            return
        rich.print(subtree.view_tree(**kwargs))


    def get_node(self, root, key: str = ''):
        if not key:
            return root
        key = key.split(os.path.sep)
        node = root
        while key:
            partial_key = key.pop(0)
            if partial_key not in node.children:
                return None
            node = node.children[partial_key]
        return node


    def insert(self, root, key: str = '', size: int = 0, is_dir = False):
        if not key:
            return root
        tokens = key.split(os.path.sep)
        file = tokens.pop()
        node = root
        while tokens:
            partial_key = tokens.pop(0)
            if partial_key not in node.children:
                x = TreeNode(value = partial_key)
                x.is_dir = True
                x.info = DirInfo()
                node.children[partial_key] = x
            node = node.children[partial_key]
        if file not in node.children:
            node.children[file] = TreeNode(value = file)
        node = node.children[file]
        node.key = key
        node.info = FileInfo()
        node.info.size = size
        if not node.info:
            node.info = FileInfo()
        node.info.update(size)
        if is_dir:
            node.is_dir = True
        return node