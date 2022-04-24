from dirman.tree.TrieST import TrieST
import pathlib, os
import prompt_toolkit as prompt
import click
from dirman.tree.info import DirInfo, FileInfo
import rich


class DirectoryTree:
    def __init__(self):
        self.tree = TrieST()
        self.index_name = TrieST()
        self.dirs = {}


    def add(self, directory: str) -> int:
        """Adds the input directory and its content to the directory tree.

        Args:
            directory (str): The directory to add.

        Returns:
            int: number of entries added.
        """
        if not os.path.exists(directory):
            click.echo(f"{directory} does not exist!")
            return 0

        path = pathlib.Path(directory)
            
        added = 0
        total_size = 0
        for p in path.rglob('*'):
            new_key_added, node = self._add(p)
            added += new_key_added
            total_size += node.info.size
            print(f"{added}. {str(p)} ({node.info.humansize()})")
        
        if path.is_dir:
            print("Adding dir:", str(path))

            _, dir_node = self.tree.insert(
                str(path), os.path.basename(path),
                root = True, is_dir = True)
            self.dirs[directory] = dir_node
            if not dir_node.info:
                dir_node.info = DirInfo()
            dir_node.info.update(total_size)
        return added

    
    def _add(self, path: pathlib.Path):
        """
        Add() helper function
        """
        name = os.path.basename(path)
        new_key_added, node = self.tree.insert(
            str(path), name, is_dir = path.is_dir())

        self.index_name.insert(name, node)
            
        if not node.info:
            node.info = FileInfo() if not path.is_dir() else DirInfo()
        node.info.update(path.stat().st_size)
        return new_key_added, node


    def delete(self, path):
        """Deletes the input path from the directory tree.

        Args:
            path (str): path can be a directory or a file.
        """
        self.tree.delete(path)


    def view(self, directory: str = ''):
        subtree = self.tree.get(directory)
        rich.print(subtree.view_tree())


if __name__ == '__main__':
    man = DirectoryTree()

    man.add('./dataset')

    man.view()

    man.delete('dataset/images')

    man.view()

    i = 0

    i += bool

    print(i)