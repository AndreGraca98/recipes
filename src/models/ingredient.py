import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from ._common import _CommonBase

if TYPE_CHECKING:
    from .recipe_ingredient import RecipeIngredient


class IngredientBase(SQLModel):
    name: str
    description: str = ""
    category: str | None = None


class Ingredient(IngredientBase, _CommonBase, table=True):
    normalized_name: str = Field(default=None, index=True, unique=True)
    object_name: str | None = Field(None, index=True)
    """image path on the filestore"""
    recipe_ingredient: "RecipeIngredient" = Relationship(back_populates="ingredient")


class IngredientPublic(IngredientBase):
    id: uuid.UUID
    normalized_name: str
    object_name: str | None


class IngredientCreate(IngredientBase): ...


class IngredientUpdate(IngredientBase):
    name: str | None = None
    normalized_name: str | None = None
    description: str | None = None
    category: str | None = None
