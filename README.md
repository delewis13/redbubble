# Redbubble coding challenge

## Installation

Requires `python3.8` or higher, due to use of the various classes from the `Typing` module.

Install dependencies on OSX / Linux via:

```cmd
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

If you wish to perform dev activities (e.g. running test cases / linting / formatting / jupyter notebook), instead install `requirements_dev.txt`

## Testing

`pytest` is used for testing.

- run via `pytest` in the terminal (must have installed `requirements_dev.txt`)
- check coverage via `pytest --cov=src` for terminal report, or `pytest --cov-report html --cov=src` for HTML report [see htmlcov/index.html]
- check general test report via `pytest --html=report.html --self-contained-html` [see report.html]
- test coverage is 100%.

## Running

Supply absolute or relative paths to cart / base_prices JSON files with:
`python run.py -c CART_PATH -b BASE_PRICES_PATH`

If an argument is not supplied for either of these variables, they fall back to using defaults of `examples/cart-4560.json` and `examples/base-prices.json` respectively.

Check help via `python run.py --help`.

## Note on validation

The instructions said validation was not needed, however I decided to include it anyway because I prefer working
with classes rather than raw dictionaries anyway. Used marshmallow to perform validation.

It was assumed that all "option values" are either strings or floats.

## Linting & Formatting

VSCode settings have been included in the repo and include the majority of our configured linting & formatting settings.
Normally would not be commited in git repo directly to remain editor-agnostic.

- `pylint` for linting. By default all rules are enabled, and some are selectively disabled as seen in `.pylintrc`. Run via `pylint src` or `python -m pylint src`.
- `black` for formatting with a line length of 119 characters. To run `black` on `src` folder: `black src --line-length 119`
- `autoflake` for removing unused imports. To run `autoflake` on `src` folder: `autoflake --remove-all-unused-imports -r -i src`
- NOTE: VSCode's inbuilt import sorting (which uses `isort` behind-the-hood) agrees with our linting rules.
