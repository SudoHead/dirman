# Introduction

A CLI **DIR**ectory **MAN**agement tool written in Python 3.


## Implementation

### Overview

The objective is to provide a simple and intuitive command line interface, similar to a bash shell. 

The *prompt_toolkit* library is used to manage the CLI experience, with features like history and selection through up/down arrows. 

For visualization, the library *rich* was used to render the tree and drawing tables.

Commands strings are processed using an handler function, which given a function mapping, will call the function with the supplied arguments. 

### Data structures

The internal data structure used to represent directories and files is an *N-ary tree*. Nodes (see ```dirman/tree/TreeNode.py```) can have multiple children, which, in turn, also can have many children.
Nodes are added recursively from the root, following the directory path by traversing the tree.

The motivation to use a tree structure is to have a convenient way of storing and navigating the directories to access files. Tree are common and well known in computer science, allowing us to use algorithms like depth-first search (DFS) or breadth-first search (BFS). Another advantage is the ability to reuse nodes for nested directories.

An additional Trie data structure stores a copy of all file names. The main purpose of the Trie is to quickly filter files by their name, avoiding to expand the search to the entire directory tree. In fact, the search runtime complexity of the Trie is $O(L)$ where $L$ is the length of the longest matching name.



## Capabilities

- **Adding directories or files:**
    ```sh
    # Adding a directory
    > add dataset

    # Adding a file
    > add dataset/file.txt
    ```

- **View:**
    ```sh
    > view
    ```
    ![Image](/dataset/images/view.png "view")


- **View with sort:** 

    - *-sort_by*: can sort by name, time, size, or date.
    - *-r*: add this option to reverse the sort.
 
    ```sh
    > view -sort_by name -r 
    ```
    ![Image](/dataset/images/view.png "view")

- **View directory**:
    ```sh
    > view dataset
    ```
    ![Image](/dataset/images/view_dir.png "view")


- **Filter:**
    
    - *--prefix*: filter the files by prefix name (i.e. ```test*```).
    - *--type*: filter the files by type (image, video, audio, text, application).
    - *-gt*: greater than n bytes.
    - *-lt*: less than n bytes.
    ```sh
    > filter dataset --prefix test --type text -gt 256 -lt 16384
    ```
    ![Image](/dataset/images/filter_test.png "view")


- **delete:**
    
    can delete files or directories.
    ```sh
    ```sh
    delete dataset
    ```


## Additional commands

Thanks to prompt_toolkit, QOL features such as command history, and clear display are easily implemented.

- **clear:**
    clears the terminal.
    ```sh
    > clear
    ```

- **history:**
    shows the command history.
    ```sh
    > history
    ```



- **Rerun old command:**
    the following command will rerun the command number 8 (as shown with ```history```).
    ```sh
    > ! 8
    ```

- **help:**
    shows the list of available commands.
    ```sh
    > help
    ```


## Install dirman

It is recommended to create a virtual environment first.

Install the setup.py:

```sh
(venv) $ pip install -e .
```

## Running dirman

Once installed, you can run dirman as CLI tool:

```sh
(venv) $ dirman
```

or as a script:

```sh
(venv) $ python dirman/dirman.py
```


## Tests

Unit testing is implemented using the *pytest* library. To run the tests:

```sh
(venv) $ python -m pytest tests
```