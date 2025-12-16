import io
from unittest.mock import patch

import pytest
from PIL import Image

from recipes.presentation.utils import save_uploaded_file


@pytest.fixture
def create_image_bytes():
    """Creates a dummy image in memory and returns it as a file-like object."""

    def _create_image(mode="RGB", size=(1200, 1200), img_format="PNG"):
        img = Image.new(mode, size, "blue")
        byte_arr = io.BytesIO()
        img.save(byte_arr, format=img_format)
        byte_arr.seek(0)
        return byte_arr

    return _create_image


@patch("recipes.presentation.utils.tempfile.gettempdir")
@patch("recipes.presentation.utils.uuid7")
def test_save_uploaded_file_resizes_converts_and_saves(
    mock_uuid, mock_gettempdir, create_image_bytes, tmp_path
):
    """
    GIVEN an uploaded image file object
    WHEN save_uploaded_file is called
    THEN it should resize the image, convert it to RGB, and save it to a temporary path.
    """
    # Arrange
    mock_uuid.return_value.hex = "test-uuid"
    mock_gettempdir.return_value = tmp_path
    large_rgba_image = create_image_bytes(mode="RGBA", size=(2000, 2000))

    # Act
    result_path = save_uploaded_file(large_rgba_image)

    # Assert
    assert result_path is not None
    expected_path = tmp_path / "ingredients_test-uuid.jpg"
    assert result_path == expected_path
    assert result_path.exists()

    # Verify image properties
    with Image.open(result_path) as saved_img:
        assert saved_img.mode == "RGB"
        assert saved_img.size[0] <= 1024
        assert saved_img.size[1] <= 1024


@patch("recipes.presentation.utils.tempfile.gettempdir")
@patch("recipes.presentation.utils.uuid7")
def test_save_uploaded_file_handles_palette_mode(
    mock_uuid, mock_gettempdir, create_image_bytes, tmp_path
):
    """
    GIVEN an uploaded image file with a 'P' (palette) mode
    WHEN save_uploaded_file is called
    THEN it should correctly convert the image to RGB before saving.
    """
    # Arrange
    mock_uuid.return_value.hex = "test-uuid-palette"
    mock_gettempdir.return_value = tmp_path

    # Create an image and convert it to 'P' mode
    img_rgb = Image.new("RGB", (100, 100))
    img_p_mode = img_rgb.convert("P", palette=Image.ADAPTIVE)
    byte_arr = io.BytesIO()
    img_p_mode.save(byte_arr, "PNG")
    byte_arr.seek(0)

    # Act
    result_path = save_uploaded_file(byte_arr)

    # Assert
    assert result_path is not None
    assert result_path.exists()
    with Image.open(result_path) as saved_img:
        assert saved_img.mode == "RGB"
