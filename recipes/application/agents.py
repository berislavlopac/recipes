from crewai import Agent


class IngredientScoutAgent:
    def __init__(self, llm):
        self.llm = llm

    def create(self) -> Agent:
        return Agent(
            role="Vision Ingredient Analyst",
            goal="Identify raw food ingredients from images with high precision.",
            backstory=(
                "You are a Google Gemini-powered vision expert. "
                "You can see details in images that others miss. "
                "You list exactly what is physically present in the photo."
            ),
            llm=self.llm,
            max_iter=1,  # Vision tasks usually only need one pass
            allow_delegation=False,
            verbose=True,
        )


class ChefAgent:
    def __init__(self, llm):
        self.llm = llm

    def create(self) -> Agent:
        return Agent(
            role="Executive Creative Chef",
            goal="Design recipes based on strict ingredient lists and user desires.",
            backstory=(
                "You are a world-class chef who minimizes waste. "
                "You take a list of ingredients and user context (e.g. 'vegan', 'quick') "
                "and hallucinate nothing—you only use what is available or common pantry staples."
            ),
            llm=self.llm,
            allow_delegation=False,
            verbose=True,
        )
