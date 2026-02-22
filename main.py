import argparse
import logging
import tempfile
from pathlib import Path

from core.config import settings
from core.image_processor import ImageProcessor
from core.gemini_client import GeminiModClient
from core.mod_builder import ModBuilder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Haydee Outfit Mod Generator via Gemini API")
    parser.add_argument("--name", type=str, required=True, help="Name of the mod (e.g., Synthwave)")
    parser.add_argument("--style", type=str, required=True, help="Visual style description (e.g., 'classic synthwave style with palm trees and a sun')")
    
    args = parser.parse_args()

    try:
        # 1. Setup Mod Directory and Builder
        builder = ModBuilder(args.name)
        builder.prepare_directory()

        # 2. Process Original Texture
        base_dds = settings.base_texture_path
        if not base_dds.exists():
            raise FileNotFoundError(f"Base texture not found at {base_dds}")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            base_png = temp_path / "base_Suit_D.png"
            generated_jpg = temp_path / "generated_Suit_D.jpg"

            # Convert base DDS to PNG for Gemini
            ImageProcessor.dds_to_png(base_dds, base_png)

            # 3. Generate New Texture via Gemini
            client = GeminiModClient()
            client.generate_texture(
                base_image_path=base_png,
                style=args.style,
                output_path=generated_jpg
            )

            # 4. Convert Result back to DDS in the new mod folder
            final_dds_path = builder.mod_dir / "Suit_D.dds"
            ImageProcessor.img_to_dds(generated_jpg, final_dds_path)

        # 5. Generate Configuration Files
        builder.generate_mtl_file()
        builder.generate_outfit_file()

        logger.info(f"Mod '{args.name}' generated successfully! You can now test it in Haydee.")

    except Exception as e:
        logger.error(f"An error occurred during mod generation: {e}")
        exit(1)

if __name__ == "__main__":
    main()
