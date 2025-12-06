# 👨‍🍳 Brightbeam Vision Chef

These are the notes about the solution for the technical task for Brightbeam.

## Implementation Choices

* **LLM Provider/Model:** Gemini 3 Pro was used for both ingredients recognition as well as for the recipe generation.
* **Framework:** CrewAI. That is the one I am most familiar with, although I'm still learning things about it.
* **Interface:** Streamlit.io was used for simplicity of implementation.
* **Programming Language:** Definitely Python preferred.

## Other Considerations:

* AI Development Workflow: While I occasionally use the Gemini plugin for Pycharm, I prefer an "offline" workflow, where the coding conversation is happening in a separate Gemini AI Studio instance, with the code copied over to the IDE manually, and modified as necessary. While Gemini (especially 3 Pro) has proven as a good assistant, it's still using quite an outdated syntax. The system instructions prompt that was used for this conversation can be found in the [GEMINI.md](GEMINI.md) file.

## Using the Solution

### Local Execution

As a first step, ensure that your Gemini API key is configured properly. For that, run this shell command from the top directory of the solution:

```shell
mkdir secrets && echo [your-gemini-api-key] > "secrets/recipes_gemini_api_key"
```

There are a few other settings that can be configured using the following variables (which can be set either on the environment, or in an `.env`) file:

* `RECIPES_DEBUG: bool = False`
* `RECIPES_VISION_MODEL: str = "gemini-3-pro-preview"`
* `RECIPES_VISION_TEMPERATURE: float = 0.0`
* `RECIPES_REASONING_MODEL: str = "gemini/gemini-3-pro-preview"` 
* `RECIPES_REASONING_TEMPERATURE: float = 0.8`

Once the API key is configured, run this command:

```shell
uv run streamlit run main.py 
```

This will install all the requirements in a Python virtual environment and execute the application locally.

### Online Deployment

The solution is also deployed online, and can be accessed at https://bl-bb-recipes.streamlit.app

