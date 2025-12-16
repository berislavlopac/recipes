from pathlib import Path
from typing import Annotated

import ollama
import PIL.Image
from crewai.tools import BaseTool
from google import genai
from pydantic import BaseModel, Field

from recipes.application.config import settings


class VisionToolInput(BaseModel):
    image_path: Annotated[str, Field(description="Absolute path to the image file.")]
    query: Annotated[str, Field(description="What to look for in the image.")]


class Gemini3VisionTool(BaseTool):
    name: str = "Gemini 3 Vision Tool"
    description: str = "Analyzes images using the latest Gemini 3 model."
    args_schema: type[BaseModel] = VisionToolInput

    @property
    def model_name(self):
        model_name = settings.VISION_GEMINI_MODEL
        if "/" in model_name:
            _, model_name = model_name.rsplit("/", maxsplit=1)
        return model_name

    def _run(self, image_path: Path | str, query: str) -> str:
        image_path = Path(image_path)
        if not image_path.exists():
            return "Error: File not found."
        img = PIL.Image.open(image_path)
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=[query, img],  # type: ignore [arg-type]
            )
        except Exception as e:  # noqa: BLE001
            return f"Vision Error: {e}"
        else:
            return response.text or ""


class OllamaVisionTool(BaseTool):
    name: str = "Ollama Vision Tool"
    description: str = "Analyzes images using a local Ollama model."
    args_schema: type[BaseModel] = VisionToolInput

    @property
    def model_name(self):
        model_name = settings.VISION_LOCAL_MODEL
        if "/" in model_name:
            _, model_name = model_name.rsplit("/", maxsplit=1)
        return model_name

    def _run(self, image_path: Path | str, query: str) -> str:
        image_path = Path(image_path)
        if not image_path.exists():
            return f"Error: Image file not found: {image_path}"
        client = ollama.Client(host=settings.VISION_LOCAL_URL)
        try:
            stream = client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": query, "images": [image_path]}],
                stream=True,
                options={
                    "num_predict": settings.VISION_HARD_STOP,
                    "temperature": settings.VISION_TEMPERATURE,
                    "repeat_penalty": 1.2,  # Penalizes repeating the same tokens.
                    "top_p": 0.9,  # Slightly restrict the token choices.
                },
            )
        except Exception as e:  # noqa: BLE001
            return f"Error processing image with Ollama: {e}"
        else:
            full_response = ""
            for chunk in stream:
                content = chunk["message"]["content"]
                if settings.DEBUG:
                    print(content, end="", flush=True)
                full_response += content

            return full_response
