from unicodedata import numeric
from dirman.tree.TreeNode import TreeNode
from dirman.tree.TrieST import TrieST
import pathlib, os
from dirman.tree.info import DirInfo, FileInfo, FileType
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
        self.root = TreeNode()
        self.trie = TrieST()
        self.added_dirs = []


    def add(self, directory: str):
        """Adds the input directory and its content to the directory tree.

        Args:
            directory (str): The directory to add.
        """
        if not os.path.exists(directory):
            path_not_exist_error(directory)
            return
        total_size = self._radd(directory)
        path = pathlib.Path(directory)
        if path.is_dir():
            root_node = self._insert_node(self.root, str(path), total_size, is_dir = True)
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
            if p.name.startswith('.') or p.is_symlink(): # avoid hidden files and symlinks
                continue
            if p.is_dir():
                total_size += self._radd(str(p))
            size = p.stat().st_size
            total_size += size
            ins_node = self._insert_node(self.root, str(p), size, is_dir = p.is_dir())
            # update the trie reference
            if not p.is_dir():
                node = self.trie.get(p.name)
                if node:
                    if not node.value:
                        node.value = []
                    node.value.append(ins_node)
                else:
                    self.trie.insert(p.name, [ins_node])
        return total_size


    def delete(self, path):
        """Deletes the input path from the directory tree.

        Args:
            path (str): path can be a directory or a file.
        """
        for i, x in enumerate(self.added_dirs):
            if x.key == path:
                del self.added_dirs[i]
        node = self._get_node(self.root, path)
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


    def view(self, directory: str = ''):
        """
        Displays the directory tree rooted at the input directory.

        Args:
            directory (str, optional): input directory. Defaults to ''.
        """        
        subtree = self._get_node(self.root, directory)
        if subtree is None:
            path_not_exist_error(directory)
            return
        rich.print(subtree.view_tree())


    def table_view(self, sort_by: str = '', r: bool = False):
        """
        Displays the added directories tree in a table.
        """
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Directory", style="bold magenta")
        table.add_column("upload time" , style="dim")
        table.add_column("last accessed", style="dim")
        table.add_column("size", justify="right")

        if sort_by == 'name' or sort_by == 'directory':
            self.added_dirs.sort(key = lambda x: x.value, reverse = r)
        elif sort_by == 'size':
            self.added_dirs.sort(key = lambda x: x.info.size, reverse = r)
        elif sort_by == 'time':
            self.added_dirs.sort(key = lambda x: x.info.upload_time, reverse = r)

        for node in self.added_dirs:
            table.add_row(
                node.value,
                node.info.upload_time,
                node.info.last_accessed,
                node.info.humansize(),
            )
        rconsole.print(table)


    def filter(
            self, 
            directory: str = '', prefix: str = '', 
            ftype: FileType = None, gt = None, lt = None,
        ):
        """
        Filters the directory tree based on the input prefix.

        Args:
            directory (str, optional): where to filter. Defaults to ''.
            prefix (str, optional): prefix pattern. Defaults to ''.
        """
        ftree = TreeNode()
        # search with a trie
        if prefix and type(prefix) == str: 
            prefix = prefix.replace("*", "")
            node_gen = self.trie.matching_prefix(prefix)

            while True:
                try:
                    node = next(node_gen)
                    for x in node.value:
                        fnode = self._insert_node(ftree, x.key, is_dir = x.is_dir)
                        fnode.info = x.info
                except StopIteration:
                    break
        else:
            ftree = self.root

        # view the filtered tree
        subtree = self._get_node(ftree, directory)
        if subtree is None:
            path_not_exist_error(directory)
            return
        rich.print(subtree.view_tree(ftype=ftype, gt=gt, lt=lt))


    def _get_node(self, root: TreeNode, key: str = '') -> TreeNode:
        """
        Returns the node of the tree rooted at the key.

        Args:
            root (TreeNode): root of the tree.
            key (str, optional): the key to search for. Defaults to ''.

        Returns:
            TreeNode: subtree rooted at the key. None if not found.
        """
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


    def _insert_node(self, root, key: str = '', size: int = 0, is_dir = False) -> TreeNode:
        """
        Inserts a new node into the tree.

        Args:
            root (TreeNode): the root of the tree.
            key (str, optional): the key to insert. Defaults to ''.
            size (int, optional): size of the file. Defaults to 0.
            is_dir (bool, optional): True if key is directory. Defaults to False.

        Returns:
            TreeNode: the added leaf.
        """
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
        if not node.info:
            node.info = FileInfo(key) if not is_dir else DirInfo()
        node.info.update(size)
        if is_dir:
            node.is_dir = True
        return node