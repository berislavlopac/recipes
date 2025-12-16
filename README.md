# 👨‍🍳 BB Vision Chef

These are the notes about the solution for the technical task.

## Implementation Choices

* **LLM Provider/Model:** Gemini 3 Pro was used for both ingredients recognition as well as for the recipe generation.
* **Framework:** CrewAI. That is the one I am most familiar with, although I'm still learning things about it.
* **Interface:** Streamlit.io was used for simplicity of implementation.
* **Programming Language:** Definitely Python preferred.

## Other Considerations:

* **AI Development Workflow:** While I occasionally use the Gemini plugin for Pycharm, I prefer an "offline" workflow, where the coding conversation is happening in a separate Gemini AI Studio instance, with the code copied over to the IDE manually, and modified as necessary. While Gemini (especially 3 Pro) has proven as a good assistant, it's still using quite an outdated syntax. The system instructions prompt that was used for this conversation can be found in the [GEMINI.md](GEMINI.md) file.

## Using the Solution

### Configuration

As a first step, ensure that your Gemini API key is configured properly. For that, run this shell command from the top directory of the solution:

```shell
mkdir secrets && echo [your-gemini-api-key] > "secrets/recipes_gemini_api_key"
```

There is a number of other settings that can be configured using environment variables (or in the `.env` file). The available variables are listed below, along with their default values.

Common settings:

* `RECIPES_DEBUG: bool = False`
* `RECIPES_COUNT: int = 3`
* `RECIPES_VISION_TEMPERATURE: float = 0.2`
* `RECIPES_REASONING_TEMPERATURE: float = 0.8`

Settings for Gemini models: 

* `RECIPES_VISION_GEMINI_MODEL: str = "gemini-3-pro-preview"`
* `RECIPES_REASONING_GEMINI_MODEL: str = "gemini/gemini-3-pro-preview"`

Settings specifically for using local LLMs:

* `RECIPES_VISION_USE_LOCAL_MODEL: bool = False`
* `RECIPES_VISION_LOCAL_MODEL: str = "ollama/llama3.2-vision"`
* `RECIPES_VISION_LOCAL_URL: str = "http://localhost:11434"`
* `RECIPES_VISION_HARD_STOP: int = 1000`
* `RECIPES_REASONING_USE_LOCAL_MODEL: bool = False`
* `RECIPES_REASONING_LOCAL_MODEL: str = "ollama/llama3.1"`
* `RECIPES_REASONING_LOCAL_URL: str = "http://localhost:11434"`

### Local Execution

Once the API key and any other variables are configured, run this command:

```shell
uv run streamlit run main.py 
```

This will install all the requirements in a Python virtual environment and execute the application locally.

### Online Deployment

The solution is also deployed online, and can be accessed at https://bl-bb-recipes.streamlit.app


## Note on Testing

Taking advantage of the extra time provided by rescheduling the interview, I have added some unit tests, primarily for the `application` layer, as well as for the tools in the `infrastructure` layer. I have used Gemini Code Assist tool, which built the tests that covered most of the required code, with only minimal manual updates necessary.

The `presentation` layer was refactored to move the image enhancement function to a separate module, which is now tested separately from the rest of the UI code.

Gemini suggested that the rest of the infrastructure layer doesn't need to be tested, with the following reasoning, which I agree with:

### Why This Code Isn't Typically Unit Tested

While we could technically test these functions by mocking the settings object and asserting that the LLM constructor is called with the correct parameters, it's generally not worth the effort for a few key reasons:

1. **No Logic, Only Configuration:** These functions contain no business logic. Their sole purpose is to read from a configuration object and pass those values to a constructor. A test would simply mirror the implementation, providing very little value.
2. **Tightly Coupled to Frameworks:** The test would be tightly coupled to the signature of the `crewai.LLM` constructor. If the library changes, the test breaks, even if our application's behaviour is still correct.
3. **Better Tested Implicitly:** The functionality of these factories is implicitly tested by the higher-level tests we've already written. For example, in `test_recipe_generation_flow_full_run`, we pass in a `mock_llm`. In a real scenario, that `mock_llm` would be an object created by one of these factory functions. The flow test ensures that as long as a valid LLM object is provided, the flow works.

In summary, the remaining infrastructure code acts as the "glue" that assembles the application at its entry point. It's part of the composition root, and its correctness is best verified through integration testing rather than unit testing.

