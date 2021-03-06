<kbd>
  <img src="https://github.com/symonk/pytest-infrastructure/blob/master/.github/.images/200px-logo.png">
</kbd>
  <p></p>

[![Build Status](https://api.travis-ci.org/symonk/pytest-infrastructure.svg?branch=master)](https://travis-ci.org/symonk/pytest-infrastructure)
[![License Apache](https://img.shields.io/badge/license-Apache%202-brightgreen.svg)](https://github.com/symonk/pytest-infrastructure/blob/master/LICENSE)
[![code coverage](https://codecov.io/gh/symonk/pytest-infrastructure/branch/master/graph/badge.svg)](https://codecov.io/gh/symonk/pytest-infrastructure)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=symonk_pytest-validate&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=symonk_pytest-validate)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## What is pytest-infrastructure? :flags:
pytest-infrastructure is a pytest (pluggy) plugin that is used to verify the infrastructure around a test environment prior to wasting time actually executing tests against it.
It is very simple, understanding the simple Infrastructure function protocol is key:

 - Infrastructure validation functions should not return or yield.
 - Infrastructure validation functions should raise an InfrastructureException upon failure.

```python
from pytest_infrastructure import infrastructure
from pytest_infrastructure import InfrastructureException

@infrastructure(order=-1)
def this_runs_multi_threaded_upfront():
    # This function is considered disabled
    ...

@infrastructure(order=0)
def this_runs_sequentially_as_first_priority():
    # order=0 (default) means the function is suitable for parallel execution
    ...


@infrastructure(ignored_on={"staging"}, order=10, name='HelloWurld')
def some_other_function_to_validate_the_stack():
    # This function is executed if --infra-env != 'staging'
    # This function is executed sequentially, with a weighted order of `10`
    # This function uses a custom name for terminal reporting etc, rather than __name__
    # This function is considered a fail as it raises an Exception: `InfrastructureException`
    raise InfrastructureException("web gui is not reachable.")
```

```bash
pytest -m my_test_marker --infrastructure-env=staging --infrastructure-thread-count=2
```

---


#### Important Notes:
 - pytest-infrastructure does **not!** support python version(s) earlier than 3 officially
 - pytest-infrastructure is open to pull requests that bring in backwards compatability but it is not a priority now
 - pytest-infrastructure does not guarantee order of isolated=False functions, order isn't even accounted for here


---


# Contributing to pytest-infrastructure

#### Setting up with tox:

 - Fork the pytest-infrastructure repository: [pytest-infrastructure](https://github.com/symonk/pytest-infrastructure/).
 - Clone your fork locally
    ```bash
        $ git clone git@github.com:YOUR_GIT_USERNAME/pytest-infrastructure.git
        $ cd pytest_infrastructure
        # now, create your own branch off "master":
        $ git checkout -b your-bugfix-branch-name master
    ```
- Install pre-commit: [pre-commit](https://pre-commit.com)
    ```bash
        $ pip install --user pre-commit
        $ pre-commit install
    ```
- Install tox
    ```bash
        pip install tox
    ```
- Run linting & tests! (linting runs on-commit automatically when you have configured pre-commit)
    ```bash
        $ tox -e linting,py38
        $ tox -e py37 -- --pdb (install in editable mode & enter debug on failure)
    ```
---

#### Setting up with a virtual environment:
 - You can create and use a virtual env like so using an editable install with [testing] extras
    ```bash
        $ python3 -m venv .venv
        $ source .venv/bin/activate  # Linux
        $ .venv/Scripts/activate.bat  # Windows
        $ pip install -e ".[testing]"
    ```
- After this you can modify files and run pytest as normal
