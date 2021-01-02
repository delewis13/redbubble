import itertools
import json
from typing import Dict, List, Union

from .models import BasePrice, Item


class CartCalculator:
    """
    Manage all cart cost calculations.
    Consists of a number of helper functions
    and the primary usecase: calculate_cart_total
    """

    def __init__(self, cart_file_path: str, base_price_file_path: str):
        with open(cart_file_path, "r") as cart_file:
            cart_dict = json.load(cart_file)

        with open(base_price_file_path, "r") as base_price_file:
            base_price_dict = json.load(base_price_file)

        self.cart: List[Item] = Item.Schema(many=True).load(cart_dict)
        self.base_prices: List[BasePrice] = BasePrice.Schema(many=True).load(base_price_dict)

        # To be instantiated later...
        self.options_order: Union[Dict[str, List[str]], None] = None
        self.prices: Union[Dict[str, int], None] = None

    def get_options_order(self) -> Dict[str, List[str]]:
        """
        Creates a dictionary where keys are product_types, and values are the list of option keys
        This list of option key creates an ordering or options, which can be used to uniquely identify products
        as `{product_type}_{option_1_key}_..._{option_n_key}`
        """
        options_order: Dict[str, List[str]] = {}
        for base_price in self.base_prices:
            product_type = base_price.product_type
            if options_order.get(product_type):
                continue

            # Sort options by alphabetical order, so that there is no confusion
            # when creating unique keys for products
            options_order[product_type] = sorted(base_price.options.keys())

        self.options_order = options_order
        return options_order

    def get_item_key(self, item: Item) -> str:
        """
        Constructs a key to uniquely refer to item based on selected options
        """
        if not self.options_order:
            raise Exception("Must call get_options_order first")

        product_type = item.product_type
        options = self.options_order[product_type]

        key = product_type
        for option in options:
            key += f"_{item.options[option]}"

        return key

    def get_prices(self) -> Dict[str, int]:
        """
        Creates a dictionary from base_prices, allowing O(1) time access
        to base prices given an items product_type and options.

        Each product and combination of options is uniquely identified
        in the dictionary by the key: `{product_type}_{option_1_value}_..._{option_n_value}`,
        where the ordering of options is determined by self.options_order
        """
        if not self.options_order:
            raise Exception("Must call get_options_order first")

        prices = {}

        for base_price in self.base_prices:
            product_type = base_price.product_type
            ordered_options = self.options_order[product_type]

            # Construct a list of lists, where each sub-list contains all
            # the option values for a given option type at the current base_price
            option_values: List[List[Union[str, float]]] = [[product_type]]
            for option in ordered_options:
                option_values.append(base_price.options[option])

            # The various permutations of option_values then gives all the possible
            # combinations of options for the current base_price
            keys_list = itertools.product(*option_values)

            for key_list in keys_list:
                key = "_".join(str(key) for key in key_list)
                prices[key] = base_price.base_price

        self.prices = prices
        return prices

    def calculate_cart_total(self) -> int:
        """
        Return the cost of the current read cart in cents
        """
        self.options_order = self.get_options_order()
        self.prices = self.get_prices()

        total = 0
        for item in self.cart:
            key = self.get_item_key(item)
            base_price = self.prices[key]
            total += (base_price + round(base_price * item.artist_markup / 100)) * item.quantity

        return total
