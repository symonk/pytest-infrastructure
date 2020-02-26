<kbd>
  <img src="https://github.com/symonk/pytest-validate/blob/master/.github/.images/pytest_validate.png">
</kbd>
  <p></p>

[![Build Status](https://api.travis-ci.org/symonk/pytest-validate.svg?branch=master)](https://travis-ci.org/symonk/pytest-validate)
[![License Apache](https://img.shields.io/badge/license-Apache%202-brightgreen.svg)](https://github.com/symonk/pytest-validate/blob/master/LICENSE)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=symonk_pytest-validate&metric=alert_status)](https://sonarcloud.io/dashboard?id=symonk_pytest-validate)
[![codecov](https://codecov.io/gh/symonk/pytest-validate/branch/master/graph/badge.svg)](https://codecov.io/gh/symonk/pytest-validate)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=symonk_pytest-validate&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=symonk_pytest-validate)
[![Find_Me LinkedIn](https://img.shields.io/badge/Find_Me-LinkedIn-brightgreen.svg)](https://www.linkedin.com/in/simonk09/)
[![Find_Me Slack](https://img.shields.io/badge/Find_Me-Slack-brightgreen.svg)](https://testersio.slack.com)

## What is pytest-validate? :flags:
Pytest-validate is a plugin for pytest that given a python module containing a list of adhering validate functions will
ensure the stack under test or runtime environment is as you expect before wasting time running test(s).  How it works is
outlined below

**pytest-validate Goals:**
 - Quickly validate a test environment or general runtime environment against X functions
 - Create an easy way for user-defined functions to be loaded and evaluated at runtime
 - When failure(s) occur provide powerful means of configuration and sensible error messages

#### Important Notes:
 - pytest-validate does **not!** support python version(s) earlier than 3.7 officially
 - pytest-validate is open to pull requests that bring in backwards compatability but it is not a priority now


 ---

 ### How It Works:
  - Create your @validate decorated functions in your own custom module.py
  - Pass the file path to your module through --validation-file=path
  - pytest-validate will automatically scan and execute your functions before running any tests

---

### Simple Example :hearts:
Example:

```python
# coming soon!
```

---

### How to Contribute to pytest-validate :rocket:
Thanks for considering contributions to the pytest-validate plugin.  To help you get started please read the following documentation.  All contributions will be strongly considered and I welcome contributions from anyone, experienced or new; the pytest ecosystem can be very confusing at first glance so if you have any questions or think you are doing something wrong, please open a PR with what you have and we can pair up on it.

 - Easier or small contributions are or will be attached to the: `easier` issue label

#### Getting started :rocket:

- Clone the repository using: `git@github.com:username/pytest-validate.git (ssh recommended over HTTPS)`
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
