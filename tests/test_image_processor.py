import pytest
from pathlib import Path
from core.image_processor import ImageProcessor

def test_dds_to_png(mocker, tmp_path):
    """Test that dds format conversion properties are set accurately."""
    mock_image_class = mocker.patch('core.image_processor.Image')
    mock_img_instance = mock_image_class.return_value.__enter__.return_value
    
    dds_path = tmp_path / "input.dds"
    png_path = tmp_path / "output.png"
    
    ImageProcessor.dds_to_png(dds_path, png_path)
    
    # Verify the Image class was initialized correctly
    mock_image_class.assert_called_once_with(filename=str(dds_path))
    
    # Verify format and save were called on instance
    assert mock_img_instance.format == 'png'
    mock_img_instance.save.assert_called_once_with(filename=str(png_path))

def test_img_to_dds(mocker, tmp_path):
    """Test that image conversion to dds executes required transformations."""
    mock_image_class = mocker.patch('core.image_processor.Image')
    mock_img_instance = mock_image_class.return_value.__enter__.return_value
    
    img_path = tmp_path / "input.jpg"
    dds_path = tmp_path / "output.dds"
    
    ImageProcessor.img_to_dds(img_path, dds_path)
    
    # Verify the Image class was initialized correctly
    mock_image_class.assert_called_once_with(filename=str(img_path))
    
    # Verify the required transformations
    mock_img_instance.resize.assert_called_once_with(2048, 2048)
    assert mock_img_instance.compression == 'dxt5'
    assert mock_img_instance.format == 'dds'
    mock_img_instance.save.assert_called_once_with(filename=str(dds_path))
