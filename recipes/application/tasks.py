from pathlib import Path

from crewai import Agent, Task

from recipes.application.config import settings
from recipes.domain.models import IngredientList, RecipeBook


def get_vision_task(image_path: Path | str, agent: Agent):
    return Task(
        description=(
            f"Use the agent's vision too to analyze the image file located at: '{image_path}'.\n"
            "Analyze the provided image using this step-by-step process:\n"
            "1. Briefly describe the scene and lighting to yourself.\n"
            "2. Scan the image from left to right.\n"
            "3. If text is visible on jars/cans, read it to confirm the item.\n"
            "4. List every edible ingredient found.\n"
            "5. Note the condition (fresh, opened, ripe) of the items."
        ),
        expected_output="A structured JSON list of verified ingredients.",
        agent=agent,
        output_pydantic=IngredientList,
    )


def get_reasoning_task(ingredients_data: IngredientList, user_preferences: str, agent: Agent):
    ing_list = [i.name for i in ingredients_data.ingredients]
    notes = ingredients_data.notes or "None"
    return Task(
        description=(
            f"Ingredients available: {ing_list}."
            f" Notes on condition: {notes}."
            f" User Preferences: '{user_preferences}'."
            f" Suggest {settings.COUNT} recipes."
            " You may assume salt, pepper, and oil are available."
        ),
        expected_output="Detailed recipes in JSON format.",
        agent=agent,
        output_pydantic=RecipeBook,
    )
