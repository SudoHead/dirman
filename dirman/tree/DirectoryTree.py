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
        f"{path} does not exist", 
        style = "bold red")


class DirectoryTree:
    def __init__(self):
        self.root = TreeNode()
        self.trie = TrieST()
        self.added_dirs = {}


    def add(self, directory: str):
        """Adds the input directory and its content to the directory tree.

        Args:
            directory (str): The directory to add.
        """
        if not os.path.exists(directory):
            path_not_exist_error(directory)
            return

        # adds all 
        if directory == '.':
            for p in pathlib.Path('.').glob('*'):
                if not p.name.startswith('.'):
                    self.add(str(p))
        else:
            total_size = self._radd(directory)
            path = pathlib.Path(directory)
            if path.is_dir():
                root_node = self._insert_node(self.root, str(path), total_size, is_dir = True)
                self.added_dirs[str(path)] = root_node


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
        # delete stale nodes from added_dirs
        for name, node in list(self.added_dirs.items()):
            if name == path or not node or not node.value:
                rconsole.print(f"Deleting{' stale' if name != path else ''} {name}", 
                    style = "red3")
                del self.added_dirs[name]


    def view(self, directory: str = '', pager: bool = False):
        """
        Displays the directory tree rooted at the input directory.

        Args:
            directory (str, optional): input directory. Defaults to ''.
        """        
        subtree = self._get_node(self.root, directory)
        if subtree is None:
            path_not_exist_error(directory)
            return
        if pager:
            with rconsole.pager(styles=True):
                rconsole.print(subtree.view_tree())
        else:
            rconsole.print(subtree.view_tree())


    def table_view(self, sort_by: str = '', r: bool = False):
        """
        Displays the added directories tree in a table.
        """
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Directory", style="bold magenta")
        table.add_column("upload time" , style="dim")
        table.add_column("last accessed", style="dim")
        table.add_column("size", justify="right")

        dir_list = self.added_dirs.items()
        if sort_by == 'name' or sort_by == 'directory':
            dir_list = sorted(self.added_dirs.items(), key = lambda xv: xv[0], reverse = r)
        elif sort_by == 'size':
            dir_list = sorted(self.added_dirs.items(), key = lambda xv: xv[1].info.size, reverse = r)
        elif sort_by == 'time':
            dir_list = sorted(self.added_dirs.items(), key = lambda xv: xv[1].info.last_accessed, reverse = r)

        for _, node in dir_list:
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
            pager: bool = False,
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
                        x.info.update()
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
        if pager:
            with rconsole.pager(styles=True):
                rconsole.print(subtree.view_tree(ftype=ftype, gt=gt, lt=lt))
        else:
            rconsole.print(subtree.view_tree(ftype=ftype, gt=gt, lt=lt))

    def _get_node(self, root: TreeNode, key: str = '') -> TreeNode:
        """
        Returns the node of the tree rooted at the key.

        Args:
            root (TreeNode): root of the tree.
            key (str, optional): the key to search for. Defaults to ''.

        Returns:
            TreeNode: subtree rooted at the key. None if not found.
        """
        if not key or key == '.':
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
        if not key or key == '.':
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
        if not node.value: # if deleted previously
            node.value = file
        if not node.info:
            node.info = FileInfo(key) if not is_dir else DirInfo()
        node.info.update(size)
        if is_dir:
            node.is_dir = True
        return node