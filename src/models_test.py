import json

import marshmallow
import pytest

from .constants import EXAMPLE_BASE_PRICES_PATH, EXAMPLE_CARTS
from .models import BasePrice, Item

item_valid = {
    "product-type": "shirt",
    "options": {"key": "value"},
    "artist-markup": 5,
    "quantity": 2,
}

item_missing_key = {
    "options": {"key": "value"},
    "artist-markup": 5,
    "quantity": 2,
}

item_additional_key = {
    "product-type": "shirt",
    "options": {"key": "value"},
    "artist-markup": 5,
    "quantity": 2,
    "additional_key": "additional_value",
}


@pytest.mark.item
class TestItem:
    """
    All tests for validating / loading data via marshmallow in Test class
    """

    def test_loads_item_valid(self):
        """
        Should load data from item_valid
        Convert kebab-case to snake_case
        Contain all required key / value pairs
        """
        item: Item = Item.Schema().loads(json.dumps(item_valid))
        assert item.product_type == item_valid["product-type"]
        assert item.artist_markup == item_valid["artist-markup"]
        assert item.options == item_valid["options"]
        assert item.quantity == item_valid["quantity"]

    def test_loads_item_additional_key(self):
        """
        Should load with an unknown key, but not add the key to the resulting object
        """
        item: Item = Item.Schema().loads(json.dumps(item_additional_key))
        assert not hasattr(item, "additional_key")

    def test_throws_item_missing_key(self):
        """
        Should throw a marshmallow validation error when missing a required key
        """
        with pytest.raises(marshmallow.ValidationError):
            Item.Schema().loads(json.dumps(item_missing_key))

    def test_loads_all_example_data(self):
        """
        Check that all example carts can be successfully loaded
        Throws validation error if any carts fail to load
        """
        for file_name in EXAMPLE_CARTS:
            with open(f"examples/{file_name}", "r") as f:
                cart = json.load(f)

            Item.Schema(many=True).load(cart)


base_price_valid = {
    "product-type": "hoodie",
    "options": {"colour": ["white", "dark"], "size": ["small", "medium"]},
    "base-price": 3800,
}

base_price_missing_key = {
    "product-type": "hoodie",
    "options": {"colour": ["white", "dark"], "size": ["small", "medium"]},
}

base_price_additional_key = {
    "product-type": "hoodie",
    "options": {"colour": ["white", "dark"], "size": ["small", "medium"]},
    "base-price": 3800,
    "additional_key": "additional_value",
}


@pytest.mark.base_price
class TestBasePrice:
    """
    All tests for validating / loading data via marshmallow in Test class
    """

    """
    All tests for validating / loading data via marshmallow in Test class
    """

    def test_loads_base_price_valid(self):
        """
        Should load data from base_price_valid
        Convert kebab-case to snake_case
        Contain all required key / value pairs
        """
        base_price: BasePrice = BasePrice.Schema().loads(json.dumps(base_price_valid))
        assert base_price.base_price == base_price_valid["base-price"]
        assert base_price.options == base_price_valid["options"]
        assert base_price.product_type == base_price_valid["product-type"]

    def test_loads_item_additional_key(self):
        """
        Should load with an unknown key, but not add the key to the resulting object
        """
        item: BasePrice = BasePrice.Schema().loads(json.dumps(base_price_additional_key))
        assert not hasattr(item, "additional_key")

    def test_throws_base_price_missing_key(self):
        """
        Should throw a marshmallow validation error when missing a required key
        """
        with pytest.raises(marshmallow.ValidationError):
            BasePrice.Schema().loads(json.dumps(base_price_missing_key))

    def test_loads_all_example_data(self):
        """
        Check that all example base-prices can be loaded
        """
        with open(EXAMPLE_BASE_PRICES_PATH, "r") as f:
            base_prices = json.load(f)

        BasePrice.Schema(many=True).load(base_prices)
