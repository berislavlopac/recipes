from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RECIPES_", env_file=".env", secrets_dir="secrets"
    )

    GEMINI_API_KEY: str
    DEBUG: bool = False
    USE_LOCAL_MODELS: bool = False

    # ingredients recognition settings
    VISION_TEMPERATURE: float = 0.0  # Low temp for factual object detection
    VISION_GEMINI_MODEL: str = "gemini-3-pro-preview"
    VISION_LOCAL_MODEL: str = "ollama/llama3.2-vision"
    VISION_LOCAL_URL: str = "http://localhost:11434"

    # recipe generation settings
    REASONING_TEMPERATURE: float = 0.8  # Higher temp for creativity
    REASONING_GEMINI_MODEL: str = "gemini/gemini-3-pro-preview"
    REASONING_LOCAL_MODEL: str = "ollama/llama3.1"
    REASONING_LOCAL_URL: str = "http://localhost:11434"


settings = Settings()  # type: ignore [call-arg]
