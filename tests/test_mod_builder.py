import pytest
from pathlib import Path
from core.mod_builder import ModBuilder

def test_mod_builder_init_valid(mock_config, mocker):
    """Test initialization with a valid mod name."""
    mocker.patch('core.mod_builder.settings', mock_config)
    builder = ModBuilder("TestOutfit")
    assert builder.mod_name == "TestOutfit"
    # Convert to string to avoid WindowsPath vs PosixPath or absolute differences
    assert str(builder.mod_dir) == str(mock_config.outfits_dir / "TestOutfit")

def test_mod_builder_init_invalid(mock_config):
    """Test that restricted names are rejected."""
    with pytest.raises(ValueError, match="Mod name cannot be 'Haydee'"):
        ModBuilder("Haydee")
    with pytest.raises(ValueError, match="Mod name cannot be 'Haydee'"):
        ModBuilder("haydee")
    with pytest.raises(ValueError, match="Mod name cannot be 'Haydee'"):
        ModBuilder("  HAYDEE  ")

def test_prepare_directory(mock_config, mocker):
    """Test that prepare_directory creates the necessary folder."""
    mocker.patch('core.mod_builder.settings', mock_config)
    builder = ModBuilder("Cyberpunk")
    
    assert not builder.mod_dir.exists()
    builder.prepare_directory()
    assert builder.mod_dir.exists()
    assert builder.mod_dir.is_dir()

def test_prepare_directory_overwrites(mock_config, mocker):
    """Test that existing directories are overwritten cleanly."""
    mocker.patch('core.mod_builder.settings', mock_config)
    builder = ModBuilder("OverwrittenMod")
    builder.prepare_directory()
    
    # Create a dummy file in the directory
    dummy_file = builder.mod_dir / "stray_file.txt"
    dummy_file.write_text("should be deleted")
    
    # Call prepare_directory again
    builder.prepare_directory()
    
    # Check that directory exists but the stray file is gone
    assert builder.mod_dir.exists()
    assert not dummy_file.exists()

def test_generate_mtl_file(mock_config, mocker):
    """Test that the .mtl file is generated with correct content."""
    mocker.patch('core.mod_builder.settings', mock_config)
    builder = ModBuilder("Synthwave")
    builder.prepare_directory()
    builder.generate_mtl_file()
    
    mtl_file = builder.mod_dir / "Suit.mtl"
    assert mtl_file.exists()
    
    content = mtl_file.read_text(encoding="utf-8")
    assert "HD_DATA_TXT 300" in content
    assert 'diffuseMap "Outfits\\Synthwave\\Suit_D.dds"' in content

def test_generate_outfit_file(mock_config, mocker):
    """Test that the .outfit file is generated with correct content."""
    mocker.patch('core.mod_builder.settings', mock_config)
    builder = ModBuilder("Retro")
    builder.prepare_directory()
    builder.generate_outfit_file()
    
    outfit_file = mock_config.outfits_dir / "Retro.outfit"
    assert outfit_file.exists() or (mock_config.haydee_path / "Outfits" / "Retro.outfit").exists()
    
    content = outfit_file.read_text(encoding="utf-8")
    assert "HD_DATA_TXT 300" in content
    assert 'name			"Retro";' in content
    assert 'material	"Outfits\\Retro\\Suit.mtl";' in content
