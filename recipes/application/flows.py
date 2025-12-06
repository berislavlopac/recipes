from typing import cast

from crewai import Crew, CrewOutput, Task
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from recipes.application.agents import ChefAgent, IngredientScoutAgent
from recipes.application.config import settings
from recipes.domain.models import IngredientList, RecipeBook
from recipes.infrastructure.llm_factory import get_reasoning_model, get_vision_model


class RecipeState(BaseModel):
    image_path: str = ""
    user_preferences: str = ""
    detected_ingredients: IngredientList | None = None
    final_recipes: RecipeBook | None = None


class RecipeGenerationFlow(Flow[RecipeState]):
    def __init__(self, image_path: str, user_preferences: str):
        super().__init__()
        self.state.image_path = image_path
        self.state.user_preferences = user_preferences

    @start()
    def analyze_image(self) -> IngredientList:
        print(f"🤖 Analyzing image: {self.state.image_path}")

        # 1. Inject Infrastructure (Scout Agent)
        llm = get_vision_model()
        agent = IngredientScoutAgent(llm).create()

        # 2. Define Vision Task
        # Gemini handles the image processing natively via the 'images' arg
        task = Task(
            description=(
                f"Use the 'Gemini Vision Tool' to analyze the image file located at: '{self.state.image_path}'.\n"
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

        # 3. Execute
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=settings.DEBUG,
            memory=False,
            cache=False,
        )
        result = cast(CrewOutput, crew.kickoff())

        self.state.detected_ingredients = cast(IngredientList, result.pydantic)
        return self.state.detected_ingredients

    @listen(analyze_image)
    def generate_recipes(self, ingredients_data: IngredientList) -> RecipeBook:
        print("🤖 Cooking recipes...")

        # 1. Inject Infrastructure
        llm = get_reasoning_model()
        agent = ChefAgent(llm).create()

        # 2. Context
        ing_list = [i.name for i in ingredients_data.ingredients]
        notes = ingredients_data.notes or "None"

        # 3. Define Reasoning Task
        task = Task(
            description=(
                f"Ingredients available: {ing_list}. "
                f"Notes on condition: {notes}. "
                f"User Preferences: '{self.state.user_preferences}'. "
                "Suggest 3 recipes. You may assume salt, pepper, and oil are available."
            ),
            expected_output="Detailed recipes in JSON format.",
            agent=agent,
            output_pydantic=RecipeBook,
        )

        # 4. Execute
        crew = Crew(agents=[agent], tasks=[task], verbose=settings.DEBUG)
        result = cast(CrewOutput, crew.kickoff())

        self.state.final_recipes = cast(RecipeBook, result.pydantic)
        return self.state.final_recipes
