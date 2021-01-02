import argparse

from src import CartCalculator
from src.constants import EXAMPLE_BASE_PRICES_PATH, EXAMPLE_CART_PATH

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate price of a basket")
    parser.add_argument(
        "--base_prices_path",
        default=EXAMPLE_BASE_PRICES_PATH,
        help="Absolute or relative path to your base prices JSON",
    )
    parser.add_argument("--cart_path", default=EXAMPLE_CART_PATH, help="Absolute or relative path to your cart JSON")
    args = parser.parse_args()

    calculator = CartCalculator(args.cart_path, args.base_prices_path)
    cart_total = calculator.calculate_cart_total()
    print(cart_total)
