import uuid

from sqlmodel import Field, SQLModel, UniqueConstraint

from ._common import _CommonBase


class RecipeIngredientLink(SQLModel, _CommonBase, table=True):
    __table_args__ = (UniqueConstraint("recipe_id", "recipe_ingredient_id"),)
    recipe_id: uuid.UUID = Field(foreign_key="recipe.id")
    recipe_ingredient_id: uuid.UUID = Field(foreign_key="recipeingredient.id")
