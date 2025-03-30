from decimal import Decimal as originalDecimal
from typing import Annotated

from pydantic import PlainSerializer

# the serialized decimal type
Decimal = Annotated[
    originalDecimal,
    PlainSerializer(
        lambda x: float(x), return_type=float, when_used="json-unless-none"
    ),
]
"""Decimal type serialized to float"""
