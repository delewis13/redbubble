# Redbubble coding challenge

## Installation

Requires `python3.8` or higher, due to use of the various classes from the `Typing` module.

Install dependencies on OSX / Linux via:

```cmd
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Linting & Formatting

VSCode settings includes the majority of our configured linting & formatting settings. Normally would not be commited in git repo directly.

- `pylint` for linting. By default all rules are enabled, and some are selectively disabled as seen in `.pylintrc`
- `black` for formatting with a line length of 119 characters. To run `black` on `src` folder: `black src --line-length 119`
- `autoflake` for removing unused imports. To run `autoflake` on `src` folder: `autoflake --remove-all-unused-imports -r -i src`
- VSCode's inbuilt import sorting (which uses `isort` behind-the-hood).
