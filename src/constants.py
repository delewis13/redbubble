"""
Constants such as directory paths and filenames
"""
import os

EXAMPLE_CARTS = ["cart-4560.json", "cart-9363.json", "cart-9500.json", "cart-11356.json"]
EXAMPLE_DIR = "examples"
EXAMPLE_BASE_PRICES_FILE = "base-prices.json"
EXAMPLE_BASE_PRICES_PATH = os.path.join(EXAMPLE_DIR, EXAMPLE_BASE_PRICES_FILE)
EXAMPLE_CART_PATH = os.path.join(EXAMPLE_DIR, EXAMPLE_CARTS[0])
