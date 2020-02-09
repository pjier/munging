[![Build Status](https://travis-ci.org/pjier/munging.svg?branch=master)](https://travis-ci.org/pjier/munging)

# Data munging

Simple Python project to solve [this task](http://codekata.com/kata/kata04-data-munging/).

Boilerplate and project structure copied from [here](https://github.com/AlexanderWillner/python-boilerplate) (Thanks, Alex Willner!)

## Available make commands

```
$ make
Some available commands:
 * run          - Run code.
 * test         - Run unit tests and test coverage.
 * doc          - Document code (pydoc).
 * clean        - Cleanup (e.g. pyc files).
 * code-style   - Check code style (pycodestyle).
 * code-lint    - Check code lints (pyflakes, pyline).
 * code-count   - Count code lines (cloc).
 * deps-install - Install dependencies (see requirements.txt).
 * deps-update  - Update dependencies (via pur).
 * feedback     - Create a GitHub issue.
```

To run the actual application:
```
$ python src/munging.py data/weather.dat
Day with minimum spread is 14
```
