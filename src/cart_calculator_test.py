import os

import pytest

from src.models import BasePrice, Item

from .cart_calculator import CartCalculator
from .constants import EXAMPLE_BASE_PRICES_PATH, EXAMPLE_CART_PATH, EXAMPLE_CARTS, EXAMPLE_DIR


@pytest.fixture
def cart_calculator() -> CartCalculator:
    return CartCalculator(EXAMPLE_CART_PATH, EXAMPLE_BASE_PRICES_PATH)


dummy_base_prices = [
    BasePrice.Schema().load(
        {
            "product-type": "product_1",
            "options": {"size": ["sm", "md"], "color": ["black", "white", "grey"]},
            "base-price": 100,
        }
    ),
    BasePrice.Schema().load(
        {
            "product-type": "product_1",
            "options": {"size": ["lg"], "color": ["red", "white"]},
            "base-price": 200,
        }
    ),
    BasePrice.Schema().load(
        {
            "product-type": "product_2",
            "options": {"size": [8.5, 9.0, 10.0], "pattern": ["crosses", "circles"]},
            "base-price": 150,
        }
    ),
]


dummy_cart = [
    Item.Schema().load(
        {"product-type": "product_1", "options": {"size": "lg", "color": "red"}, "artist-markup": 100, "quantity": 2}
    ),
    Item.Schema().load(
        {"product-type": "product_2", "options": {"size": 9, "pattern": "circles"}, "artist-markup": 0, "quantity": 1}
    ),
]

dummy_options_order = {"product_1": ["color", "size"], "product_2": ["pattern", "size"]}
dummy_prices = {
    "product_1_black_sm": 100,
    "product_1_white_sm": 100,
    "product_1_grey_sm": 100,
    "product_1_black_md": 100,
    "product_1_white_md": 100,
    "product_1_grey_md": 100,
    "product_1_red_lg": 200,
    "product_1_white_lg": 200,
    "product_2_crosses_8.5": 150,
    "product_2_circles_8.5": 150,
    "product_2_crosses_9.0": 150,
    "product_2_circles_9.0": 150,
    "product_2_crosses_10.0": 150,
    "product_2_circles_10.0": 150,
}


@pytest.mark.cart_calculator
class TestCartCalculator:
    def test_init(self, cart_calculator: CartCalculator):
        """
        Test the calculator instantiates correctly
        """
        assert isinstance(cart_calculator.cart[0], Item)
        assert isinstance(cart_calculator.base_prices[0], BasePrice)
        assert cart_calculator.options_order is None
        assert cart_calculator.prices is None

    def test_calculate_cart_total(self):
        """
        Test that the correct cart total is reported for all example carts
        """
        for example_cart_file_name in EXAMPLE_CARTS:
            expected_total = int(example_cart_file_name.split(".")[0].split("-")[1])
            total = CartCalculator(
                os.path.join(EXAMPLE_DIR, example_cart_file_name), EXAMPLE_BASE_PRICES_PATH
            ).calculate_cart_total()
            assert total == expected_total

    def test_get_options_order(self, cart_calculator: CartCalculator):
        cart_calculator.base_prices = dummy_base_prices

        options_order = cart_calculator.get_options_order()

        assert options_order == dummy_options_order

    def test_get_prices(self, cart_calculator: CartCalculator):
        cart_calculator.base_prices = dummy_base_prices

        cart_calculator.get_options_order()
        prices = cart_calculator.get_prices()

        assert sorted(prices.keys()) == sorted(dummy_prices.keys())

        for key, value in prices.items():
            assert dummy_prices[key] == value

    def test_get_item_key(self, cart_calculator: CartCalculator):
        cart_calculator.base_prices = dummy_base_prices
        cart_calculator.get_options_order()
        key = cart_calculator.get_item_key(dummy_cart[0])
        assert key == "product_1_red_lg"

    def test_throws(self, cart_calculator: CartCalculator):
        """
        Test various functions throw if they are called too early
        """
        with pytest.raises(Exception):
            cart_calculator.get_item_key(dummy_cart[0])

        with pytest.raises(Exception):
            cart_calculator.get_prices()
