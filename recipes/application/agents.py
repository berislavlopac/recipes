from crewai import LLM, Agent

from recipes.application.config import settings
from recipes.infrastructure import vision


def create_food_analyst(llm: LLM) -> Agent:
    return Agent(
        role="Forensic Food Analyst",
        goal="Analyze food images with extreme precision, reading labels and identifying produce state.",
        backstory=(
            "You are a meticulous inventory specialist. "
            "You do not guess. If a label is visible, you read it to confirm the ingredient. "
            "You distinguish between fresh produce (e.g., 'Roma Tomato') and packaged goods. "
            "You ignore non-food items like plates, counters, or cutlery."
        ),
        llm=llm,
        tools=[vision.get_tool()],
        max_iter=1,  # Vision tasks usually only need one pass
        allow_delegation=False,
        verbose=settings.DEBUG,
    )


def create_chef(llm: LLM) -> Agent:
    return Agent(
        role="Executive Creative Chef",
        goal="Design recipes based on strict ingredient lists and user desires.",
        backstory=(
            "You are a world-class chef who minimizes waste. "
            "You take a list of ingredients and user context (e.g. 'vegan', 'quick') "
            "and hallucinate nothing—you only use what is available or common pantry staples."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=settings.DEBUG,
    )
