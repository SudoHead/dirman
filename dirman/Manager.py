from dirman.TrieST import TrieST
import pathlib, os
import prompt_toolkit as prompt
import click

class Manager:
    def __init__(self):
        self.folders = TrieST()


    def add(self, folder):
        if not os.path.exists(folder):
            click.echo(f"{folder} does not exist!")
            return
        path = pathlib.Path(folder)
        print("adding:", str(path))
        if path.is_dir:
            self.folders.insert(str(path), os.path.basename(path), \
                root = True, is_dir = True)
        for p in path.rglob('*'):
            print("adding:", str(p))
            self.folders.insert(str(p), os.path.basename(p), is_dir = p.is_dir())


    def delete(self, path):
        self.folders.delete(path)


    def view(self, folder: str = '') -> str:
        value_nodes = list(self.folders.matching_prefix(folder))
        content = [' ' * 4 * node.tree_level + f"|- {node.value}" \
                for node in value_nodes]
        return '\n'.join(content)



if __name__ == '__main__':
    man = Manager()

    man.add('./dataset')

    man.view()

    man.delete('dataset/images')

    man.view()