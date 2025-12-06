from typing import Annotated

from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: Annotated[str, Field(description="Name of the identified ingredient")]
    confidence: Annotated[str, Field(description="High, Medium, or Low confidence level")]
    category: Annotated[str, Field(description="Produce, Dairy, Meat, Pantry, etc.")]


class IngredientList(BaseModel):
    image_description: Annotated[
        str,
        Field(description="First, describe the image scene in detail to confirm you see it."),
    ]
    ingredients: list[Ingredient]
    notes: Annotated[
        str | None, Field(description="Any observations about freshness or state")
    ] = None


class Recipe(BaseModel):
    title: str
    difficulty: Annotated[str, Field(description="Easy, Medium, Hard")]
    prep_time: str
    cooking_time: str
    calories_per_serving: int | None = None
    ingredients_needed: Annotated[
        list[str], Field(description="List of ingredients including quantities")
    ]
    instructions: Annotated[list[str], Field(description="Step-by-step cooking instructions")]
    why_it_fits: Annotated[
        str,
        Field(description="Brief explanation of why this fits the user's preference"),
    ]


class RecipeBook(BaseModel):
    recipes: list[Recipe]
    chef_comment: Annotated[str, Field(description="Overall comment from the chef agent")]
