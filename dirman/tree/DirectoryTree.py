from dirman.tree.TrieST import TrieST
import pathlib, os
import prompt_toolkit as prompt
import click


class DirectoryTree:
    def __init__(self):
        self.tree = TrieST()
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
        if path.is_dir:
            print("Adding dir:", str(path))
            
            new_key_added, _ = self.tree.insert(
                str(path), os.path.basename(path),
                root = True, is_dir = True)
            
        added = 0
        for p in path.rglob('*'):
            new_key_added, _ = self.tree.insert(
                str(p), os.path.basename(p), is_dir = p.is_dir())
            added += new_key_added
            print(f"{added}", str(p))
        return added



    def delete(self, path):
        """Deletes the input path from the directory tree.

        Args:
            path (str): path can be a directory or a file.
        """
        self.tree.delete(path)


    def view(self, directory: str = '') -> str:
        value_nodes = list(self.tree.matching_prefix(directory))
        content = [' ' * 4 * node.tree_level + f"|- {node.value}" \
                for node in value_nodes]
        return '\n'.join(content)



if __name__ == '__main__':
    man = DirectoryTree()

    man.add('./dataset')

    man.view()

    man.delete('dataset/images')

    man.view()

    i = 0

    i += bool

    print(i)