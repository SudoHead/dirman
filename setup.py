from dirman.__init__ import __version__
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    lines = f.readlines()
    requirements = [r.strip() for r in lines]

setup(
    description='dirman: cli tool for managing directories',
    author='Max Xiang',
    download_url='https://github.com/SudoHead/dirman',
    name='dirman',
    version=__version__,
    license='LICENSE',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'dirman=dirman.dirman:main',
        ]
    },
    packages=find_packages('.'),
)