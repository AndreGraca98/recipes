import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from ._common import _CommonBase
from .ingredient import IngredientCreate, IngredientPublic
from .recipe_ingredient_to_recipe_link import RecipeIngredientLink
from .types.unit import Unit

if TYPE_CHECKING:
    from .ingredient import Ingredient
    from .recipe import Recipe


class RecipeIngredientBase(SQLModel):
    quantity: Decimal
    unit: Unit


class RecipeIngredient(RecipeIngredientBase, _CommonBase, table=True):
    ingredient_id: uuid.UUID = Field(foreign_key="ingredient.id")
    ingredient: "Ingredient" = Relationship(back_populates="recipe_ingredient")

    recipes: list["Recipe"] = Relationship(
        back_populates="recipe_ingredients", link_model=RecipeIngredientLink
    )


class RecipeIngredientPublic(RecipeIngredientBase):
    id: uuid.UUID
    ingredient: IngredientPublic


class RecipeIngredientCreate(RecipeIngredientBase):
    ingredient: IngredientCreate


class RecipeIngredientUpdate(RecipeIngredientBase):
    quantity: Decimal | None = None
    unit: Unit | None = None
    recipe_id: uuid.UUID | None = None
    ingredient_id: uuid.UUID | None = None
