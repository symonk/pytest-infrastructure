# Contributing to pytest-infrastructure

#### Setting up with tox:

 - Fork the pytest-infrastructure repository: [pytest-infrastructure](https://github.com/symonk/pytest-infrastructure/).
 - Clone your fork locally
    ```console
        $ git clone git@github.com:YOUR_GIT_USERNAME/pytest-infrastructure.git
        $ cd pytest_infrastructure
        # now, create your own branch off "master":
        $ git checkout -b your-bugfix-branch-name master
    ```
- Install pre-commit: [pre-commit](https://pre-commit.com)
    ```console
        $ pip install --user pre-commit
        $ pre-commit install
    ```
- Install tox
    ```console
        pip install tox
    ```
- Run linting & tests! (linting runs on-commit automatically when you have configured pre-commit)
    ```console
        $ tox -e linting,py38
        $ tox -e py37 -- --pdb (install in editable mode & enter debug on failure)
    ```
---

#### Setting up with a virtual environment:
 - You can create and use a virtual env like so using an editable install with [testing] extras
    ```console
        $ python3 -m venv .venv
        $ source .venv/bin/activate  # Linux
        $ .venv/Scripts/activate.bat  # Windows
        $ pip install -e ".[testing]"
    ```
- After this you can modify files and run pytest as normal
