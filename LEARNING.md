# Learning & Exploration Challenge

As defined in the task description, I have decided to try running models locally as the "exploration" part of my task. I really like the idea of not depending on commercial model providers and being able to use custom ones, whether open source or home-traiuned ones.

## Learning Documentation

### What was new to you about this technology/approach?

I previously used only the commercial LLM providers (primarily Gemini). I wanted to see how would open source models compare to them, both in terms of performance and accuracy.


### What resources did you use to learn it?

Honestly, the best resource was Gemini 3 Pro. I was able to ask questions as if talking to an expert, which was much more efficient than trying to figure things out by reading the documentation; it even have tips that are not clearly marked in the documentation (e.g that the default CrewAI `VisionTool` is heavily biased to ChatGPT, so it's better to build a custom one.)

There were a couple occasions where the code it suggested used an outdated (albeit still correct) syntax, and in a few cases it misunderstood my intent; although that was likely due to my unclear prompts.


### What challenges did you encounter and how did you resolve them?

The main challenge was getting the local models to run smoothly and without glitches like endless loops.

The first challenge was that my main laptop doesn't have a dedicated GPU, so the models were executed in CPU mode, which obviously reduced performance and maxxed all of my cores. This was resolved by setting Ollama up on my gaming laptop, which has a nice and powerful NVidia GPU.

The second challenge was tuning the vision model (Llama 3.2 Vision) to prevent issues like infinite lists and hallucinations.

### What insights did you gain that would be valuable to share with the team?

This is probably no big news for experienced AI engineers, but I learned that, from the perspective of the agentic flow execution, it doesn't really matter which model is being used. All models are essentially hiding behind dedicated server - such as Ollama or LM Studio when run locally, so the main difference is setting up the right model names and URLs, as well as setting up the right tools in the agentic code.

That being said, there is a significant difference in the performance of different models and quality of their outputs.

Unsurprisingly, there is a significant difference in performance when running models in CPU-mode.

Additionally, the vision models (like Ollama 3.2 Vision) are very moody and need to be carefully tuned to avoid issues like endless lists and repeating tokens.

In terms of accuracy in recognising ingredients, I was able to get Ollama 3.2 Vision to have acceptable results, although nowhere near to the results of Gemini 3 Pro. My "gold standard" was the photo with three jars of food - Gemini was able to correctly identify the ingredients (rice, oats, lentils) - especially after improving the photo quality using `pillow` - while Ollama Vision misidentified the ones present (salt instead of rice, tomato instead of lentils, and probably chicken breast instead of oats), and invented a couple of new oned (like basil and olive oil). Interestingly enough, Gemini didn't recognise the egg packets on one of the photos, while Ollama did.


### What would you investigate further with more time?

Ideally, I would explore what would it be like to have a model that is specifically trained with the goal of recognising food ingredients from photographs. While this would probably be an overkill for a "toy" use case like this, there is a great potential in such custom models for specific purposes like medical diagnosis, analysing satellite images and the like.


## Handoff Documentation

To run the solution with the local LLMs, follow these steps:

1. [Install ollama](https://ollama.com/download) on the local machine.
2. Prepare the required models:
   ```shell
   ollama pull llama3.2-vision
   ollama pull llama3.1
   ```
3. Set the environment variables (using an `.env` file is the easiest):
   ```shell
   export RECIPES_VISION_USE_LOCAL_MODEL=true
   export RECIPES_REASONING_USE_LOCAL_MODEL=true
   ```
4. Run the Streamlit application locally:
   ```shell
   uv run streamlit run main.py
   ```
   
It is possible to experiment by enabling only one of the vision and reasoning steps, as well as other variables listed in [README.md](README.md).

