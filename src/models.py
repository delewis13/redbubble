from typing import ClassVar, Dict, List, Type, Union

import marshmallow_dataclass
from marshmallow import EXCLUDE, Schema

"""
Provide models for various data objects required throughout script.
Using classes rather than raw dicts allows for better intellisense & typechecking
Stay DRY by using marshmallow_dataclass instead of vanilla marshmallow

Models assume that the values of options are either strings or floats.
Not specified in project briefing.
"""


def kebabcase(s):
    """
    Change kebab-case to snake_case
    """
    return s.replace("_", "-")


class KebabCaseSchema(Schema):
    """Schema that uses kebab-case for its external representation
    and snake-case for its internal representation.
    """

    class Meta:
        """
        Exclude unknown keys
        """

        unknown = EXCLUDE

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = kebabcase(field_obj.data_key or field_name)


@marshmallow_dataclass.dataclass(base_schema=KebabCaseSchema)
class Item:
    """
    Load individual items according to Schema
    """

    product_type: str
    options: Dict[str, Union[str, float]]
    artist_markup: int
    quantity: int
    Schema: ClassVar[Type[Schema]] = Schema


@marshmallow_dataclass.dataclass(base_schema=KebabCaseSchema)
class BasePrice:
    """
    Load individual base prices according to Schema
    """

    product_type: str
    options: Dict[str, List[Union[str, float]]]
    base_price: int
    Schema: ClassVar[Type[Schema]] = Schema
