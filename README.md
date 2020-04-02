<kbd>
  <img src="https://github.com/symonk/pytest-infrastructure/blob/master/.github/.images/pytest_infrastructure.png">
</kbd>
  <p></p>

[![Build Status](https://api.travis-ci.org/symonk/pytest-validate.svg?branch=master)](https://travis-ci.org/symonk/pytest-validate)
[![License Apache](https://img.shields.io/badge/license-Apache%202-brightgreen.svg)](https://github.com/symonk/pytest-infrastructure/blob/master/LICENSE)
[![code coverage](https://codecov.io/gh/symonk/pytest-infrastructure/branch/master/graph/badge.svg)](https://codecov.io/gh/symonk/pytest-infrastructure)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=symonk_pytest-validate&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=symonk_pytest-validate)
[![Find_Me LinkedIn](https://img.shields.io/badge/Find_Me-LinkedIn-brightgreen.svg)](https://www.linkedin.com/in/simonk09/)
[![Find_Me Slack](https://img.shields.io/badge/Find_Me-Slack-brightgreen.svg)](https://testersio.slack.com)

## What is pytest-infrastructure? :flags:
Pytest-infrastructure is a plugin for pytest that given a python module containing a list of adhering @infrastructure decorated functions will
ensure the stack under test or runtime environment is as you expect before wasting time running test(s).  How it works is
outlined below

**pytest-infrastructure; How it works:**

    write your own python module containing functions decorated by the @infrastructure decorator
    pass the path to your file to pytest via --infrastructure-file=~./path/of/file.py
    pytest-infrastructure will do the rest, ensuring the runtime environment is adaquate to carry out the test run
    if it is not, pytest-infrastructure aims to be clean and concise in telling you why it failed
    @infrastructure is fully loaded with capabilities; supports parallelism and supports xdist

---


#### Important Notes:
 - pytest-infrastructure does **not!** support python version(s) earlier than 3 officially
 - pytest-infrastructure is open to pull requests that bring in backwards compatability but it is not a priority now


---

### Simple Example :hearts:
Example:

```python
from pytest_infrastructure import infrastructure

@infrastructure(order=1, enabled=True, not_on_env='staging', isolated=True)
def some_function_to_validate_the_environment():
    # This will be run in parallel; order plays no part when isolated=True is set
    # This will be executed first, order=1 (n.b => order 0 is considered priority and negative order is equal to 0


@infrastructure(enabled=True, exclude_on_environments='production', isolated=False)
def some_other_function_to_validate_the_stack():
    # This will be run sequentially in parallel
    pass
```

---

### How to Contribute to pytest-infrastructure :rocket:
Thanks for considering contributions to the pytest-infrastructure plugin.  To help you get started please read the following documentation.  All contributions will be strongly considered and I welcome contributions from anyone, experienced or new; the pytest ecosystem can be very confusing at first glance so if you have any questions or think you are doing something wrong, please open a PR with what you have and we can pair up on it.

 - Easier or small contributions are or will be attached to the: `easier` issue label

#### Getting started :rocket:

- Clone the repository using: `git@github.com:username/pytest-infrastructure.git (ssh recommended over HTTPS)`
- Open the cloned folder in your IDE of choice, I would recommend `Pycharm` (or if you are hardcore and dont use an IDE)
- Create a branch or if you prefer to work on forks do that
- Push change(s) for issue/tickets you wish to solve
- Open a PR

`If you are solving an issue, please include closes #issue-number in the commit message, for example: "fixes #1"`

#### PR Guidelines :rocket:
Under **NO** circumstances will any PR be accepted with the following:

- Failing travis CI build / tests
- Decrease in unit test coverage percentage

If your PR is failing on either of these two, it will only be considered mergable when they have been rectified (unless there is a core travis issue in which I will try to resolve immediately)

---
