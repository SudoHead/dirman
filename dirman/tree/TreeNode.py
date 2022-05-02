from math import inf
from queue import Queue
from rich.markup import escape
from rich.tree import Tree as ViewTree
from dirman.tree.info import FileType

class TreeNode:
    def __init__(self, key = None, value = None, info = None):
        self.children = {}
        self.key = key
        self.value = value
        self.is_dir = False
        self.info = info


    def reset(self):
        """
        Reset the node to its initial state.
        """
        self.children = {}
        self.key = None
        self.value = None
        self.is_dir = False
        if self.info:
            self.info.update(0)


    def view_tree(
            self, 
            ftype: FileType = None, gt = -inf, lt = inf, 
            vtree: ViewTree = None) -> ViewTree:
        """Walk the tree using DFS.

        Args:
            ftype (FileType, optional): file type. Defaults to None.
            gt (numeric, optional): greater than. Defaults to inf.
            lt (numeric, optional): less than. Defaults to -inf.
            vtree (ViewTree, optional): rich.tree for rendering. Defaults to None.

        Returns:
            ViewTree: the rich.tree to render.
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
            and (ftype is None or self.info.type == ftype) \
            and self.info.size \
            and (self.info.size < lt \
            and self.info.size > gt):
            vtree.add(self.value + f" ({str(self.info)})")

        self.info.update()
        for child in self.children.values():
            child.view_tree(ftype, gt, lt, vtree)
        return vtree


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(key={self.key}, "\
            + f"value={self.value}, is_dir={self.is_dir}, "\
            + f"info={str(self.info)})"