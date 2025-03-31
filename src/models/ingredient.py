import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from ._common import _CommonBase

if TYPE_CHECKING:
    from .recipe_ingredient import RecipeIngredient


class IngredientBase(SQLModel):
    name: str = Field(index=True, unique=True)
    description: str = ""


class Ingredient(IngredientBase, _CommonBase, table=True):
    recipe_ingredient: "RecipeIngredient" = Relationship(back_populates="ingredient")


class IngredientPublic(IngredientBase):
    id: uuid.UUID


class IngredientCreate(IngredientBase): ...


class IngredientUpdate(IngredientBase):
    name: str | None = None
    description: str | None = None
