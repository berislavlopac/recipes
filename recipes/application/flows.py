from typing import cast

from crewai import LLM, Crew, Task
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from recipes.application import agents
from recipes.application.config import settings
from recipes.application.tasks import get_reasoning_task, get_vision_task
from recipes.domain.models import IngredientList, RecipeBook
from recipes.infrastructure import reasoning, vision


class RecipeState(BaseModel):
    image_path: str = ""
    user_preferences: str = ""
    detected_ingredients: IngredientList | None = None
    final_recipes: RecipeBook | None = None


class RecipeGenerationFlow(Flow[RecipeState]):
    def __init__(
        self, image_path: str, user_preferences: str, vision_llm: LLM, reasoning_llm: LLM
    ):
        super().__init__()
        self.state.image_path = image_path
        self.state.user_preferences = user_preferences
        self.vision_llm = vision_llm
        self.reasoning_llm = reasoning_llm

    @start()
    def analyze_image(self) -> IngredientList:
        print(f"🤖 Analyzing image: {self.state.image_path}")

        # 1. Inject Infrastructure (Scout Agent)
        agent = agents.create_food_analyst(self.vision_llm)

        # 2. Define Vision Task
        task = get_vision_task(self.state.image_path, agent)

        # 3. Execute
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=settings.DEBUG,
            memory=False,
            cache=False,
        )
        result = crew.kickoff()

        self.state.detected_ingredients = cast(IngredientList, result.pydantic)  # type: ignore [union-attr]
        return self.state.detected_ingredients

    @listen(analyze_image)
    def generate_recipes(self, ingredients_data: IngredientList) -> RecipeBook:
        print("🤖 Cooking recipes...")

        # 1. Inject Infrastructure
        agent = agents.create_chef(self.reasoning_llm)

        # 2. Define Reasoning Task
        task = get_reasoning_task(ingredients_data, self.state.user_preferences, agent)

        # 3. Execute
        crew = Crew(agents=[agent], tasks=[task], verbose=settings.DEBUG)
        result = crew.kickoff()

        self.state.final_recipes = cast(RecipeBook, result.pydantic)  # type: ignore [union-attr]
        return self.state.final_recipes
