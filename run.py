import argparse

from src.cart_calculator import CartCalculator
from src.constants import EXAMPLE_BASE_PRICES_PATH, EXAMPLE_CART_PATH

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate price of a basket")
    parser.add_argument(
        "-b",
        "--base_prices_path",
        default=EXAMPLE_BASE_PRICES_PATH,
        help="Absolute or relative path to your base prices JSON",
    )
    parser.add_argument("-c", "--cart_path", default=EXAMPLE_CART_PATH, help="Absolute or relative path to your cart JSON")
    args = parser.parse_args()

    print(f'Calculating cost of cart: {args.cart_path} given base prices: {args.base_prices_path}')

    calculator = CartCalculator(args.cart_path, args.base_prices_path)
    cart_total = calculator.calculate_cart_total()
    print(f'Total cost of cart: {cart_total}')
