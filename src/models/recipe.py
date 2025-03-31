import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from ._common import _CommonBase
from .recipe_ingredient import RecipeIngredientCreate, RecipeIngredientPublic
from .recipe_ingredient_to_recipe_link import RecipeIngredientLink

if TYPE_CHECKING:
    from .recipe_ingredient import RecipeIngredient


class RecipeBase(SQLModel):
    name: str = Field(index=True, unique=True)
    description: str = ""
    prep_time: int | None = None
    cook_time: int | None = None
    servings: int


class Recipe(RecipeBase, _CommonBase, table=True):
    recipe_ingredients: list["RecipeIngredient"] = Relationship(
        back_populates="recipes", link_model=RecipeIngredientLink
    )


class RecipePublic(RecipeBase):
    id: uuid.UUID
    recipe_ingredients: list[RecipeIngredientPublic]


class RecipeCreate(RecipeBase):
    recipe_ingredients: list[RecipeIngredientCreate]


class RecipeUpdate(RecipeBase):
    name: str | None = None
    description: str | None = None
    prep_time: int | None = None
    cook_time: int | None = None
    servings: int | None = None
