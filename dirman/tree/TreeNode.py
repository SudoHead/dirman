from math import inf
from queue import Queue
from rich.markup import escape
from rich.tree import Tree as ViewTree

class TreeNode:
    def __init__(self, key = None, value = None, tree_level = 1, info = None):
        self.children = {}
        self.key = key
        self.value = value
        self.is_dir = False
        self.tree_level = tree_level
        self.info = info


    def reset(self):
        self.children = {}
        self.key = None
        self.value = None
        self.is_dir = False
        if self.info:
            self.info.update(0)


    def view_tree(self, type = None, gt = -inf, lt = inf, 
        vtree: ViewTree = None):
        """Walk the tree using DFS.

        Args:
            type (_type_, optional): _description_. Defaults to None.
            gt (_type_, optional): _description_. Defaults to inf.
            lt (_type_, optional): _description_. Defaults to -inf.
            vtree (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        if not vtree:
            name = f"[bold green]:mag: View"
            if self.value:
                name = f"[bold magenta]:mag: {self.value}"
            vtree = ViewTree(
                name,
                guide_style="bold bright_blue",
            )
        elif self.is_dir:
            vtree = vtree.add(
                f"[bold magenta]:open_file_folder: {escape(self.value)}")
        elif self.value \
            and (type is None or (self.info and self.info.type.value == type)) \
            and self.info.size < lt \
            and self.info.size > gt:
            vtree.add(self.value + f" ({str(self.info)})")

        for child in self.children.values():
            child.view_tree(type, gt, lt, vtree)
        return vtree


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(key={self.key}, "\
            + f"value={self.value}, is_dir={self.is_dir}, "\
            + f"tree_level={self.tree_level}, info={str(self.info)})"