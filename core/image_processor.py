import logging
from pathlib import Path
from wand.image import Image

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Handles image conversions between DDS and standard formats."""

    @staticmethod
    def dds_to_png(dds_path: Path, png_path: Path) -> None:
        """Converts a DDS texture to PNG format for API processing."""
        logger.info(f"Converting {dds_path.name} to PNG...")
        with Image(filename=str(dds_path)) as img:
            img.format = 'png'
            img.save(filename=str(png_path))
        logger.info(f"Successfully saved to {png_path}")

    @staticmethod
    def img_to_dds(img_path: Path, dds_path: Path) -> None:
        """Converts a generated image (PNG/JPG) back to DDS format."""
        logger.info(f"Converting {img_path.name} to DDS...")
        with Image(filename=str(img_path)) as img:
            # Force size 2048x2048 before saving
            img.resize(2048, 2048)
            # DXT5 compression is standard for diffuse textures with details/alpha
            img.compression = 'dxt5'
            img.format = 'dds'
            img.save(filename=str(dds_path))
        logger.info(f"Successfully saved to {dds_path}")
