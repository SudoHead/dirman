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