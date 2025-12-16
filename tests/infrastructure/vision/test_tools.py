from pathlib import Path
from unittest.mock import MagicMock, patch

from recipes.infrastructure.vision.tools import Gemini3VisionTool, OllamaVisionTool


@patch("recipes.infrastructure.vision.tools.settings")
@patch("recipes.infrastructure.vision.tools.genai.Client")
@patch("recipes.infrastructure.vision.tools.PIL.Image")
@patch("recipes.infrastructure.vision.tools.Path.exists")
def test_gemini3_vision_tool_run(
    mock_path_exists, mock_pil_image, mock_genai_client, mock_settings
):
    """
    GIVEN a Gemini3VisionTool instance
    WHEN the _run method is called with a valid image path
    THEN it should call the Gemini API and return the text response.
    """
    mock_settings.GEMINI_API_KEY = "fake-api-key"
    mock_path_exists.return_value = True
    mock_image_obj = MagicMock()
    mock_pil_image.open.return_value = mock_image_obj

    mock_model_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "This is a tomato."
    mock_model_instance.models.generate_content.return_value = mock_response
    mock_genai_client.return_value = mock_model_instance

    tool = Gemini3VisionTool()
    query = "What is in this image?"
    image_path = "/fake/path/image.jpg"

    # Act
    result = tool._run(image_path=image_path, query=query)

    # Assert
    mock_path_exists.assert_called_once()
    mock_pil_image.open.assert_called_with(Path(image_path))
    mock_genai_client.assert_called_once_with(api_key="fake-api-key")
    mock_model_instance.models.generate_content.assert_called_once_with(
        model=mock_settings.VISION_GEMINI_MODEL, contents=[query, mock_image_obj]
    )
    assert result == "This is a tomato."


@patch("recipes.infrastructure.vision.tools.ollama.Client")
@patch("recipes.infrastructure.vision.tools.Path.exists")
def test_ollama_vision_tool_run(mock_path_exists, mock_ollama_client):
    """
    GIVEN an OllamaVisionTool instance
    WHEN the _run method is called with a valid image path
    THEN it should call the Ollama client and return the streamed response.
    """
    # Arrange
    mock_path_exists.return_value = True

    mock_stream_chunk = {"message": {"content": "This is a tomato."}}
    mock_ollama_instance = MagicMock()
    mock_ollama_instance.chat.return_value = [mock_stream_chunk]
    mock_ollama_client.return_value = mock_ollama_instance

    tool = OllamaVisionTool()
    query = "What is in this image?"
    image_path = "/fake/path/image.jpg"

    # Act
    result = tool._run(image_path=image_path, query=query)

    # Assert
    mock_path_exists.assert_called_once()
    mock_ollama_client.assert_called_once()
    mock_ollama_instance.chat.assert_called_once()
    assert result == "This is a tomato."


def test_gemini3_vision_tool_file_not_found():
    """
    GIVEN a Gemini3VisionTool instance
    WHEN the _run method is called with a non-existent image path
    THEN it should return an error message.
    """
    # Arrange
    tool = Gemini3VisionTool()
    with patch("recipes.infrastructure.vision.tools.Path.exists", return_value=False):
        # Act
        result = tool._run(image_path="/fake/path/nonexistent.jpg", query="test")

        # Assert
        assert "Error: File not found" in result
