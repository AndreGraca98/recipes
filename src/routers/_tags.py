from dataclasses import asdict, dataclass

TAGS_METADATA: list[dict[str, str]] = []
"""Metadata for tags, used for OpenAPI documentation"""


@dataclass
class _Tag:
    """Tag metadata for OpenAPI documentation"""

    name: str
    description: str

    def __post_init__(self):
        global TAGS_METADATA
        TAGS_METADATA.append(asdict(self))


V1 = _Tag("V1", "Version 1 of the API").name
Recipe = _Tag("Recipe", "Recipe").name
RecipeIngredient = _Tag("RecipeIngredient", "RecipeIngredient").name
Ingredient = _Tag("Ingredients", "Ingredients").name
