from crewai import Crew, Task
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from recipes.application.agents import ChefAgent, IngredientScoutAgent
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
    def analyze_image(self):
        print(f"🤖 Gemini Flash analyzing: {self.state.image_path}")

        # 1. Inject Infrastructure (Gemini Flash)
        llm = get_vision_model()
        agent = IngredientScoutAgent(llm).create()

        # 2. Define Vision Task
        # Gemini handles the image processing natively via the 'images' arg
        task = Task(
            description="Look at the image and output a structured list of every food ingredient you see.",
            expected_output="JSON structure of ingredients.",
            agent=agent,
            output_pydantic=IngredientList,
            images=[self.state.image_path],
        )

        # 3. Execute
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()

        self.state.detected_ingredients = result.pydantic
        return result.pydantic

    @listen(analyze_image)
    def generate_recipes(self, ingredients_data):
        print("🤖 Gemini Pro cooking recipes...")

        # 1. Inject Infrastructure (Gemini Pro)
        llm = get_reasoning_model()
        agent = ChefAgent(llm).create()

        # 2. Context
        ing_list = [i.name for i in self.state.detected_ingredients.ingredients]
        notes = self.state.detected_ingredients.notes or "None"

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
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()

        self.state.final_recipes = result.pydantic
        return result.pydantic
