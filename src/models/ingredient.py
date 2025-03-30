import uuid

from sqlmodel import Field, SQLModel

from ._common import _CommonBase


class IngredientBase(SQLModel):
    name: str = Field(index=True, unique=True)
    description: str = ""


class Ingredient(IngredientBase, _CommonBase, table=True): ...


class IngredientPublic(IngredientBase):
    id: uuid.UUID


class IngredientCreate(IngredientBase): ...


class IngredientUpdate(IngredientBase):
    name: str | None = None
    description: str | None = None
