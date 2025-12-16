from unittest.mock import MagicMock, patch

import pytest
from crewai import LLM

from recipes.application.flows import RecipeGenerationFlow
from recipes.domain.models import Ingredient, IngredientList, Recipe, RecipeBook


@pytest.fixture
def mock_llm():
    """Fixture to create a mock LLM object."""
    return MagicMock(spec=LLM)


@patch("recipes.application.flows.Crew")
def test_recipe_generation_flow_full_run(mock_crew_class, mock_llm):
    """
    GIVEN a RecipeGenerationFlow instance
    WHEN the flow is kicked off and both tasks are mocked to succeed
    THEN the flow should complete and the final state should contain both ingredients and recipes.
    """
    # Arrange
    # 1. Mock the result of the first crew's kickoff (vision task)
    mock_vision_result = MagicMock()
    mock_vision_result.pydantic = IngredientList(
        image_description="A test image",
        ingredients=[Ingredient(name="Tomato", confidence="High", category="Produce")],
        notes="Looks fresh",
    )

    # 2. Mock the result of the second crew's kickoff (reasoning task)
    mock_reasoning_result = MagicMock()
    mock_reasoning_result.pydantic = RecipeBook(
        recipes=[
            Recipe(
                title="Tomato Soup",
                difficulty="Easy",
                prep_time="5 mins",
                cooking_time="15 mins",
                ingredients_needed=["1 Tomato"],
                instructions=["Slice tomato", "Boil water", "Combine"],
                why_it_fits="It's a simple recipe.",
            )
        ],
        chef_comment="A classic dish.",
    )

    # Configure the mock Crew instances to return the mock results in sequence
    mock_crew_instance = MagicMock()
    mock_crew_instance.kickoff.side_effect = [
        mock_vision_result,
        mock_reasoning_result,
    ]
    mock_crew_class.return_value = mock_crew_instance

    # 3. Instantiate the flow
    flow = RecipeGenerationFlow(
        image_path="/fake/path/image.jpg",
        user_preferences="Something simple",
        vision_llm=mock_llm,
        reasoning_llm=mock_llm,
    )

    # Act
    # The kickoff method will trigger the @start and @listen decorators
    final_result = flow.kickoff()

    # Assert
    # 1. Check that kickoff was called twice (once for each task)
    assert mock_crew_instance.kickoff.call_count == 2

    # 2. Check the intermediate state after the first task
    assert flow.state.detected_ingredients is not None
    assert flow.state.detected_ingredients.ingredients[0].name == "Tomato"

    # 3. Check the final state and the result of the flow
    assert flow.state.final_recipes is not None
    assert flow.state.final_recipes.recipes[0].title == "Tomato Soup"
    assert isinstance(final_result, RecipeBook)
    assert final_result.recipes[0].title == "Tomato Soup"
