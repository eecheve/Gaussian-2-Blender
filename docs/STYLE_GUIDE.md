# Python Style Guide

This style guide outlines the coding conventions for this repository. Please follow these guidelines to ensure consistency and readability.
*NOTE: this tool was created with the aid of an LLM tool*

## General Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) for coding style.
- Use meaningful variable and function names.
- Keep code modular and reusable.
- Write clear and concise comments where necessary.

## Formatting

- Use **4 spaces per indentation level** (no tabs).
- Limit lines to **79 characters**.
- Use blank lines to separate logical sections of code.
- Use **snake_case** for function and variable names.
- Use **UPPER_CASE** for constants.
- Use **CamelCase** for class names.

## Imports

- Use absolute imports instead of relative imports.
- Place imports at the top of the file.
- Group imports in the following order:
  1. Standard library imports
  2. Third-party library imports
  3. Local application imports

Example:
```python
import os
import sys

import numpy as np

from my_project.module import my_function
```

## Docstrings & Comments

- Use **docstrings** for all public modules, functions, classes, and methods.
- Use triple double-quotes for docstrings (`"""`).
- Keep comments relevant and concise.

Example:
```python
def add_numbers(a, b):
    """Return the sum of two numbers."""
    return a + b
```

## Naming Conventions

- Functions & Variables: `snake_case`
- Classes: `CamelCase`
- Constants: `UPPER_CASE`
- Private methods and variables should start with an underscore (`_`).

## Testing

- Write unit tests for all critical code.
- Use `pytest` or `unittest` frameworks.
- Place tests in a `tests/` directory.

## Version Control

- Use meaningful commit messages (e.g., `fix: resolve issue #123`).
- Keep PRs focused and small.

By following this guide, we ensure clean, readable, and maintainable code. Happy coding! 🚀

