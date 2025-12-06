from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RECIPES_", env_file=".env", secrets_dir="secrets"
    )

    GEMINI_API_KEY: str
    DEBUG: bool = False

    # ingredients recognition settings
    VISION_MODEL: str = "gemini-3-pro-preview"
    VISION_TEMPERATURE: float = 0.0  # Low temp for factual object detection

    # recipe generation settings
    REASONING_MODEL: str = "gemini/gemini-3-pro-preview"
    REASONING_TEMPERATURE: float = 0.8  # Higher temp for creativity


settings = Settings()  # type: ignore [call-arg]
