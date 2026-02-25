import pytest
from pathlib import Path
from unittest.mock import MagicMock, call
from haydee_outfit_gen.gemini_client import GeminiModClient

def test_gemini_client_init(mock_config, mocker):
    """Test client initializes with the correct API key."""
    mock_genai = mocker.patch('haydee_outfit_gen.gemini_client.genai')
    
    client = GeminiModClient()
    mock_genai.Client.assert_called_once_with(api_key="fake_test_key_123")

def test_generate_texture_success_parts_image(mock_config, mocker, tmp_path):
    """Test successful image generation and saving using standard parts.image."""
    mock_genai = mocker.patch('haydee_outfit_gen.gemini_client.genai')
    
    # Setup mock client
    mock_client_instance = MagicMock()
    mock_genai.Client.return_value = mock_client_instance
    
    # Setup mock response with candidate -> content -> parts -> image
    mock_response = MagicMock()
    mock_candidate = MagicMock()
    mock_part = MagicMock()
    
    mock_part.image = MagicMock()
    mock_part.image.image_bytes = b"fake_image_data"
    
    mock_candidate.content.parts = [mock_part]
    mock_response.candidates = [mock_candidate]
    
    mock_client_instance.models.generate_content.return_value = mock_response
    
    # Initialize our client wrapper and call
    client = GeminiModClient()
    
    from PIL import Image
    base_image = tmp_path / "base.png"
    Image.new('RGB', (1, 1)).save(base_image)
    output_image = tmp_path / "output.jpg"
    
    client.generate_texture(base_image, "Synthwave", output_image)
    
    # Assertions
    assert output_image.exists()
    assert output_image.read_bytes() == b"fake_image_data"
    mock_client_instance.models.generate_content.assert_called_once()

def test_generate_texture_success_inline_data(mock_config, mocker, tmp_path):
    """Test successful image generation and saving using inline_data fallback."""
    mock_genai = mocker.patch('haydee_outfit_gen.gemini_client.genai')
    
    mock_client_instance = MagicMock()
    mock_genai.Client.return_value = mock_client_instance
    
    mock_response = MagicMock()
    mock_candidate = MagicMock()
    mock_part = MagicMock()
    
    # Delete the standard custom payload structure to force fallback
    del mock_part.image
    mock_part.inline_data = MagicMock()
    mock_part.inline_data.data = b"fake_inline_data"
    
    mock_candidate.content.parts = [mock_part]
    mock_response.candidates = [mock_candidate]
    
    mock_client_instance.models.generate_content.return_value = mock_response
    
    client = GeminiModClient()
    
    from PIL import Image
    base_image = tmp_path / "base.png"
    Image.new('RGB', (1, 1)).save(base_image)
    output_image = tmp_path / "output.jpg"
    
    client.generate_texture(base_image, "Retro", output_image)
    
    assert output_image.exists()
    assert output_image.read_bytes() == b"fake_inline_data"

def test_generate_texture_no_image_returned(mock_config, mocker, tmp_path):
    """Test that a RuntimeError is raised if no image is found in response."""
    mock_genai = mocker.patch('haydee_outfit_gen.gemini_client.genai')
    
    mock_client_instance = MagicMock()
    mock_genai.Client.return_value = mock_client_instance
    
    # Create an empty response mock that doesn't trigger the success conditions
    mock_response = MagicMock()
    mock_response.candidates = []
    mock_response.parts = []
    
    mock_client_instance.models.generate_content.return_value = mock_response
    
    client = GeminiModClient()
    
    from PIL import Image
    base_image = tmp_path / "base.png"
    Image.new('RGB', (1, 1)).save(base_image)
    output_image = tmp_path / "output.jpg"
    
    with pytest.raises(RuntimeError, match="No image was returned from Gemini API."):
        client.generate_texture(base_image, "FailingStyle", output_image)
